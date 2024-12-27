# -*- encoding: utf-8 -*-
"""
Reg-Pilot-Filer Servcie
filer.core.basing module

Database support
"""
import os
from collections import namedtuple
from dataclasses import dataclass, asdict, field
from typing import List

from keri.core import coring
from keri.db import dbing, subing, koming
from keri.db.subing import CesrIoSetSuber
from keri.help.helping import nowUTC
from typing import Optional
import datetime


@dataclass
class ReportStats:
    """ Report statistics dataclass for tracking"""
    submitter: str = None
    filename: str = None
    status: str = None
    contentType: str = None
    size: int = 0
    message: str = ""

# Report Statuses.
Reportage = namedtuple("Reportage", "accepted verified failed")

# Referencable report status enumeration
ReportStatus = Reportage(accepted="accepted", verified="verified", failed="failed")

@dataclass
class UploadStatus:
    """ Upload status dataclass for tracking"""
    status: str = None
    saids: List[str] = None

def delete_upload_status(fdb, status: ReportStats, said: str):
    """
    Add status to the status database

    Parameters:
        status (str): status of the report
        said (str): SAID of the report

    """
    statuses = fdb.stts.get(keys=(status,))
    if statuses and said in statuses.saids:
        statuses.saids.remove(said)
        fdb.stts.pin(keys=(status,), val=statuses)
    
def save_upload_status(fdb, status: ReportStats, said: str):
    """
    Add status to the status database

    Parameters:
        status (str): status of the report
        said (str): SAID of the report

    """
    statuses = fdb.stts.get(keys=(status,))
    if not statuses:
        statuses = UploadStatus(status=status, saids=[])
    statuses.saids.append(said)
    statuses.saids = list(set(statuses.saids))
    fdb.stts.pin(keys=(status,), val=statuses)
    

class FilerBaser(dbing.LMDBer):
    """
    FilerBaser stores report verification status alongside AIDs

    """
    TailDirPath = "keri/fdb"
    AltTailDirPath = ".filer/fdb"
    TempPrefix = "keri_fdb_"
    KERIBaserMapSizeKey = "KERI_BASER_MAP_SIZE"

    def __init__(self, name="fdb", headDirPath=None, reopen=True, **kwa):
        """  Create filer database

        Parameters:
            headDirPath (str): override for root directory
            reopen (bool): True means call reopen on database object creations
            kwa (dict): additional key word argument pass through for database initialization
        """

        # Report database linking AID of uploader to SAID of uploaded report
        self.rpts = None

        # Report SAIDs indexed by status
        self.stts = None

        # Data chunks for uploaded report, indexed by SAID plus chunk index
        self.imgs = None

        # Komer instance of ReportStats data class, keyed by SAID
        self.stats = None

        if (mapSize := os.getenv(self.KERIBaserMapSizeKey)) is not None:
            try:
                self.MapSize = int(mapSize)
            except ValueError:
                print("KERI_BASER_MAP_SIZE must be an integer value >1!")
                raise

        super(FilerBaser, self).__init__(name=name, headDirPath=headDirPath, reopen=reopen, **kwa)

    def reopen(self, **kwa):
        """  Opens database environment and initializes all sub-dbs

        Parameters:
            **kwa (dict): key word argument pass through for database initialization

        Returns:
            env: database environment for filer database

        """
        super(FilerBaser, self).reopen(**kwa)


        # Report database linking AID of uploader to DIG of uploaded report
        self.rpts = CesrIoSetSuber(db=self, subkey='rpts.', klas=coring.Diger)

        # Report DIGs indexed by status
        self.stts = koming.Komer(db=self, subkey='stts.', schema=UploadStatus)

        # Data chunks for uploaded report, indexed by DIG plus chunk index
        self.imgs = self.env.open_db(key=b'imgs.')

        # Komer instance of ReportStats data class, keyed by SAID
        self.stats = koming.Komer(db=self,
                                  subkey='stats.',
                                  schema=ReportStats)

        return self.env
