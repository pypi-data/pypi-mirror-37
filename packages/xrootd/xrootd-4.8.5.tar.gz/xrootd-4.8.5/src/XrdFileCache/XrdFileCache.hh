#ifndef __XRDFILECACHE_CACHE_HH__
#define __XRDFILECACHE_CACHE_HH__
//----------------------------------------------------------------------------------
// Copyright (c) 2014 by Board of Trustees of the Leland Stanford, Jr., University
// Author: Alja Mrak-Tadel, Matevz Tadel, Brian Bockelman
//----------------------------------------------------------------------------------
// XRootD is free software: you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// XRootD is distributed in the hope that it will be useful,
// but WITHOUT ANY emacs WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU Lesser General Public License
// along with XRootD.  If not, see <http://www.gnu.org/licenses/>.
//----------------------------------------------------------------------------------
#include <string>
#include <list>

#include "Xrd/XrdScheduler.hh"
#include "XrdVersion.hh"
#include "XrdSys/XrdSysPthread.hh"
#include "XrdOuc/XrdOucCache2.hh"
#include "XrdOuc/XrdOucCallBack.hh"
#include "XrdCl/XrdClDefaultEnv.hh"
#include "XrdFileCacheFile.hh"
#include "XrdFileCacheDecision.hh"

class XrdOucStream;
class XrdSysError;
class XrdSysTrace;

namespace XrdCl {
class Log;
}
namespace XrdFileCache {
class File;
class IO;
}


namespace XrdFileCache
{
//----------------------------------------------------------------------------
//! Contains parameters configurable from the xrootd config file.
//----------------------------------------------------------------------------
struct Configuration
{
   Configuration() :
      m_hdfsmode(false),
      m_data_space("public"),
      m_meta_space("public"),
      m_diskUsageLWM(-1),
      m_diskUsageHWM(-1),
      m_purgeInterval(300),
      m_bufferSize(1024*1024),
      m_RamAbsAvailable(0),
      m_NRamBuffers(-1),
      m_prefetch_max_blocks(10),
      m_hdfsbsize(128*1024*1024),
      m_flushCnt(100)
   {}

   bool m_hdfsmode;                     //!< flag for enabling block-level operation

   std::string m_username;              //!< username passed to oss plugin
   std::string m_data_space;            //!< oss space for data files
   std::string m_meta_space;            //!< oss space for metadata files (cinfo)

   long long m_diskUsageLWM;            //!< cache purge low water mark
   long long m_diskUsageHWM;            //!< cache purge high water mark
   int       m_purgeInterval;           //!< sleep interval between cache purges

   long long m_bufferSize;              //!< prefetch buffer size, default 1MB
   long long m_RamAbsAvailable;         //!< available from configuration
   int       m_NRamBuffers;             //!< number of total in-memory cache blocks, cached
   size_t    m_prefetch_max_blocks;     //!< maximum number of blocks to prefetch per file

   long long m_hdfsbsize;               //!< used with m_hdfsmode, default 128MB
   long long m_flushCnt;                //!< nuber of unsynced blcoks on disk before flush is called
};

struct TmpConfiguration
{
   std::string m_diskUsageLWM;
   std::string m_diskUsageHWM;
   std::string m_flushRaw;

   TmpConfiguration() :
      m_diskUsageLWM("0.90"), m_diskUsageHWM("0.95"), m_flushRaw("100")
   {}
};

//----------------------------------------------------------------------------
//! Attaches/creates and detaches/deletes cache-io objects for disk based cache.
//----------------------------------------------------------------------------
class Cache : public XrdOucCache2
{
public:
   //---------------------------------------------------------------------
   //! Constructor
   //---------------------------------------------------------------------
   Cache();

   //---------------------------------------------------------------------
   //! Obtain a new IO object that fronts existing XrdOucCacheIO.
   //---------------------------------------------------------------------
   using XrdOucCache2::Attach;

   virtual XrdOucCacheIO2 *Attach(XrdOucCacheIO2 *, int Options = 0);

   //---------------------------------------------------------------------
   //! Number of cache-io objects atteched through this cache.
   //---------------------------------------------------------------------
   virtual int isAttached();

   //---------------------------------------------------------------------
   // Virtual function of XrdOucCache2. Used to pass environmental info.
   virtual void EnvInfo(XrdOucEnv &theEnv);

   //---------------------------------------------------------------------
   // Virtual function of XrdOucCache2. Used for deferred open.
   virtual int  Prepare(const char *url, int oflags, mode_t mode);


   // virtual function of XrdOucCache2::Stat()
   virtual int  Stat(const char *url, struct stat &sbuff);

   //--------------------------------------------------------------------
   //! \brief Makes decision if the original XrdOucCacheIO should be cached.
   //!
   //! @param & URL of file
   //!
   //! @return decision if IO object will be cached.
   //--------------------------------------------------------------------
   bool Decide(XrdOucCacheIO*);

   //------------------------------------------------------------------------
   //! Reference XrdFileCache configuration
   //------------------------------------------------------------------------
   const Configuration& RefConfiguration() const { return m_configuration; }


   //---------------------------------------------------------------------
   //! \brief Parse configuration file
   //!
   //! @param logger             xrootd logger
   //! @param config_filename    path to configuration file
   //! @param parameters         optional parameters to be passed
   //!
   //! @return parse status
   //---------------------------------------------------------------------
   bool Config(XrdSysLogger *logger, const char *config_filename, const char *parameters);

   //---------------------------------------------------------------------
   //! Singleton access.
   //---------------------------------------------------------------------
   static Cache &GetInstance();

   //---------------------------------------------------------------------
   //! Version check.
   //---------------------------------------------------------------------
   static bool VCheck(XrdVersionInfo &urVersion) { return true; }

   //---------------------------------------------------------------------
   //! Thread function running disk cache purge periodically.
   //---------------------------------------------------------------------
   void CacheDirCleanup();

   //---------------------------------------------------------------------
   //! Add downloaded block in write queue.
   //---------------------------------------------------------------------
   void AddWriteTask(Block* b, bool from_read);

   //---------------------------------------------------------------------
   //!  \brief Remove blocks from write queue which belong to given prefetch.
   //! This method is used at the time of File destruction.
   //---------------------------------------------------------------------
   void RemoveWriteQEntriesFor(File *f);

   //---------------------------------------------------------------------
   //! Separate task which writes blocks from ram to disk.
   //---------------------------------------------------------------------
   void ProcessWriteTasks();

   bool RequestRAMBlock();

   void RAMBlockReleased();

   void RegisterPrefetchFile(File*);
   void DeRegisterPrefetchFile(File*);

   File* GetNextFileToPrefetch();

   void Prefetch();

   XrdOss* GetOss() const { return m_output_fs; }

   bool HaveActiveFileWithLocalPath(std::string);
   
   File* GetFile(const std::string&, IO*, long long off = 0, long long filesize = 0);

   void ReleaseFile(File*);

   void ScheduleFileSync(File* f) { schedule_file_sync(f, false); }

   void FileSyncDone(File*);
   
   XrdSysTrace* GetTrace() { return m_trace; }

private:
   bool ConfigParameters(std::string, XrdOucStream&, TmpConfiguration &tmpc);
   bool ConfigXeq(char *, XrdOucStream &);
   bool xdlib(XrdOucStream &);
   bool xtrace(XrdOucStream &);

   static Cache     *m_factory;         //!< this object
   static 
   XrdScheduler     *schedP;

   XrdSysError       m_log;             //!< XrdFileCache namespace logger
   XrdSysTrace      *m_trace;
   const char       *m_traceID;

   XrdOucCacheStats  m_stats;           //!<
   XrdOss           *m_output_fs;       //!< disk cache file system

   std::vector<XrdFileCache::Decision*> m_decisionpoints;       //!< decision plugins

   std::map<std::string, long long> m_filesInQueue;

   Configuration m_configuration;           //!< configurable parameters

   XrdSysCondVar m_prefetch_condVar;        //!< central lock for this class

   XrdSysMutex m_RAMblock_mutex;            //!< central lock for this class
   int         m_RAMblocks_used;
   bool        m_isClient;                  //!< True if running as client

   struct WriteQ
   {
      WriteQ() : condVar(0), size(0) {}
      XrdSysCondVar     condVar;      //!< write list condVar
      size_t            size;         //!< cache size of a container
      std::list<Block*> queue;        //!< container
   };

   WriteQ m_writeQ;

   // active map
   typedef std::map<std::string, File*> ActiveMap_t;
   typedef ActiveMap_t::iterator        ActiveMap_i;

   ActiveMap_t  m_active;
   XrdSysMutex  m_active_mutex;

   void inc_ref_cnt(File*, bool lock);
   void dec_ref_cnt(File*);

   void schedule_file_sync(File*, bool ref_cnt_already_set);

   // prefetching
   typedef std::vector<File*>  PrefetchList;
   PrefetchList m_prefetchList;
};

}

#endif
