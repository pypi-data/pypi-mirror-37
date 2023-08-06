#ifndef __XRDFILECACHE_FILE_HH__
#define __XRDFILECACHE_FILE_HH__
//----------------------------------------------------------------------------------
// Copyright (c) 2014 by Board of Trustees of the Leland Stanford, Jr., University
// Author: Alja Mrak-Tadel, Matevz Tadel
//----------------------------------------------------------------------------------
// XRootD is free software: you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// XRootD is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU Lesser General Public License
// along with XRootD.  If not, see <http://www.gnu.org/licenses/>.
//----------------------------------------------------------------------------------

#include "XrdCl/XrdClXRootDResponses.hh"
#include "XrdCl/XrdClDefaultEnv.hh"

#include "XrdOuc/XrdOucCache2.hh"
#include "XrdOuc/XrdOucIOVec.hh"

#include "XrdFileCacheInfo.hh"
#include "XrdFileCacheStats.hh"

#include <string>
#include <map>

class XrdJob;
class XrdOucIOVec;

namespace XrdCl
{
class Log;
}

namespace XrdFileCache
{
class BlockResponseHandler;
class DirectResponseHandler;
class IO;

struct ReadVBlockListRAM;
struct ReadVChunkListRAM;
struct ReadVBlockListDisk;
struct ReadVChunkListDisk;
}


namespace XrdFileCache
{

class File;

class Block
{
public:
   std::vector<char>   m_buff;
   long long           m_offset;
   File               *m_file;
   bool                m_prefetch;
   int                 m_refcnt;
   int                 m_errno;                         // stores negative errno
   bool                m_downloaded;

   Block(File *f, long long off, int size, bool m_prefetch) :
      m_offset(off), m_file(f), m_prefetch(m_prefetch), m_refcnt(0),
      m_errno(0), m_downloaded(false)
   {
      m_buff.resize(size);
   }

   char*     get_buff(long long pos = 0) { return &m_buff[pos]; }
   int       get_size()   { return (int) m_buff.size(); }
   long long get_offset() { return m_offset; }

   bool is_finished() { return m_downloaded || m_errno != 0; }
   bool is_ok()       { return m_downloaded; }
   bool is_failed()   { return m_errno != 0; }

   void set_error_and_free(int err)
   {
      m_errno = err;
      std::vector<char> x;
      m_buff.swap(x);
   }
};

// ================================================================

class BlockResponseHandler : public XrdOucCacheIOCB
{
public:
   Block *m_block;

   BlockResponseHandler(Block *b) : m_block(b) {}

   virtual void Done(int result);
};

// ================================================================

class DirectResponseHandler : public XrdOucCacheIOCB
{
public:
   XrdSysCondVar m_cond;
   int m_to_wait;
   int m_errno;

   DirectResponseHandler(int to_wait) : m_cond(0), m_to_wait(to_wait), m_errno(0) {}

   bool is_finished() { XrdSysCondVarHelper _lck(m_cond); return m_to_wait == 0; }
   bool is_ok()       { XrdSysCondVarHelper _lck(m_cond); return m_to_wait == 0 && m_errno == 0; }
   bool is_failed()   { XrdSysCondVarHelper _lck(m_cond); return m_errno != 0; }

   virtual void Done(int result);
};

// ================================================================

class File
{
public:
   //------------------------------------------------------------------------
   //! Constructor.
   //------------------------------------------------------------------------
   File(IO *io, const std::string &path, long long offset, long long fileSize);

   //------------------------------------------------------------------------
   //! Destructor.
   //------------------------------------------------------------------------
   ~File();

   void BlockRemovedFromWriteQ(Block*);
   //! Open file handle for data file and info file on local disk.
   bool Open();

   //! Vector read from disk if block is already downloaded, else ReadV from client.
   int ReadV (const XrdOucIOVec *readV, int n);

   int Read(char* buff, long long offset, int size);

   //----------------------------------------------------------------------
   //! \brief Data and cinfo files are open.
   //----------------------------------------------------------------------
   bool isOpen() const { return m_is_open; }

   //----------------------------------------------------------------------
   //! \brief Initiate close. Return true if still IO active.
   //! Used in XrdPosixXrootd::Close()
   //----------------------------------------------------------------------
   bool ioActive();
   
   //----------------------------------------------------------------------
   //! \brief Flags that detach stats should be written out in final sync.
   //! Called from CacheIO upon Detach.
   //----------------------------------------------------------------------
   void RequestSyncOfDetachStats();

   //----------------------------------------------------------------------
   //! \brief Returns true if any of blocks need sync.
   //! Called from Cache::dec_ref_cnt on zero ref cnt
   //----------------------------------------------------------------------
   bool FinalizeSyncBeforeExit();

   //----------------------------------------------------------------------
   //! Sync file cache inf o and output data with disk
   //----------------------------------------------------------------------
   void Sync();

   //----------------------------------------------------------------------
   //! Reference to prefetch statistics.
   //----------------------------------------------------------------------
   Stats& GetStats() { return m_stats; }

   void ProcessBlockResponse(Block* b, int res);
   void WriteBlockToDisk(Block* b);

   void Prefetch();

   float GetPrefetchScore() const;

   //! Log path
   const char* lPath() const;

   std::string& GetLocalPath() { return m_filename; }

   XrdSysTrace*  GetTrace();

   long long GetFileSize() { return m_fileSize; }

   IO*  SetIO(IO* io);
   void ReleaseIO();

   // These three methods are called under Cache's m_active lock
   int get_ref_cnt() { return   m_ref_cnt; }
   int inc_ref_cnt() { return ++m_ref_cnt; }
   int dec_ref_cnt() { return --m_ref_cnt; }

private:
   enum PrefetchState_e { kOff=-1, kOn, kHold, kStopped, kComplete };

   int            m_ref_cnt;            //!< number of references from IO or sync
   
   bool           m_is_open;            //!< open state

   IO            *m_io;                 //!< original data source
   XrdOssDF      *m_output;             //!< file handle for data file on disk
   XrdOssDF      *m_infoFile;           //!< file handle for data-info file on disk
   Info           m_cfi;                //!< download status of file blocks and access statistics

   std::string    m_filename;           //!< filename of data file on disk
   long long      m_offset;             //!< offset of cached file for block-based operation
   long long      m_fileSize;           //!< size of cached disk file for block-based operation

   // fsync
   std::vector<int>  m_writes_during_sync;
   int  m_non_flushed_cnt;
   bool m_in_sync;

   typedef std::list<int>        IntList_t;
   typedef IntList_t::iterator   IntList_i;

   typedef std::list<Block*>     BlockList_t;
   typedef BlockList_t::iterator BlockList_i;

   typedef std::map<int, Block*> BlockMap_t;
   typedef BlockMap_t::iterator  BlockMap_i;


   BlockMap_t m_block_map;

   XrdSysCondVar m_downloadCond;

   Stats m_stats;                   //!< cache statistics, used in IO detach

   PrefetchState_e m_prefetchState;

   int   m_prefetchReadCnt;
   int   m_prefetchHitCnt;
   float m_prefetchScore;              //cached
   
   bool  m_detachTimeIsLogged;

   static const char *m_traceID;
   bool overlap(int blk,               // block to query
                long long blk_size,    //
                long long req_off,     // offset of user request
                int req_size,          // size of user request
                // output:
                long long &off,        // offset in user buffer
                long long &blk_off,    // offset in block
                long long &size);
   // Read
   Block* PrepareBlockRequest(int i, bool prefetch);
   
   void   ProcessBlockRequests(BlockList_t& blks);

   int    RequestBlocksDirect(DirectResponseHandler *handler, IntList_t& blocks,
                              char* buff, long long req_off, long long req_size);

   int    ReadBlocksFromDisk(IntList_t& blocks,
                             char* req_buf, long long req_off, long long req_size);

   // VRead
   bool VReadValidate     (const XrdOucIOVec *readV, int n);
   bool VReadPreProcess   (const XrdOucIOVec *readV, int n,
                           ReadVBlockListRAM&  blks_to_process,
                           ReadVBlockListDisk& blks_on_disk,
                           std::vector<XrdOucIOVec>& chunkVec);
   int  VReadFromDisk     (const XrdOucIOVec *readV, int n,
                           ReadVBlockListDisk& blks_on_disk);
   int  VReadProcessBlocks(const XrdOucIOVec *readV, int n,
                           std::vector<ReadVChunkListRAM>& blks_to_process,
                           std::vector<ReadVChunkListRAM>& blks_rocessed);

   long long BufferSize();
   void AppendIOStatToFileInfo();

   void inc_ref_count(Block*);
   void dec_ref_count(Block*);
   void free_block(Block*);

   int  offsetIdx(int idx);
};

}

#endif
