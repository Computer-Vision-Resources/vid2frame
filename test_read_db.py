import sys
import time
import lmdb
import h5py
import numpy as np
from PIL import Image
from cStringIO import StringIO

db = sys.argv[1]

t0 = time.time()
N = 0

if db.endswith('hdf5'):
    frame_db = h5py.File(db, 'r')
    for vid in frame_db:
        db_vid = frame_db[vid]
        for fid in db_vid:
            s = np.asarray(db_vid[fid]).tostring()
            try:
                img = Image.open(StringIO(s))
                N += 1
            except:
                print 'reading failed for %s/%s' % (vid, fid)

else:  # assuming LMDB
    frame_db = lmdb.open(db, readonly=True)

    with frame_db.begin() as txn:
        cur = txn.cursor()
        f = cur.first()
        while f:
            k,v = cur.key(), cur.value()

            try:
                img = Image.open(StringIO(v))
                N += 1
            except:
                print 'reading failed for %s' % k

            f = cur.next()

print 'Num image:', N
print 'Size:', img.size
print 'Time:', time.time() - t0



