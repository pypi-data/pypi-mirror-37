This test file test the rewind command in several situations.

Global setup
============

  $ . $TESTDIR/testlib/common.sh
  $ cat >> $HGRCPATH <<EOF
  > [ui]
  > interactive = true
  > [phases]
  > publish=False
  > [extensions]
  > evolve =
  > EOF

  $ hg init rewind-testing-base
  $ cd rewind-testing-base
  $ echo a > root
  $ hg add root
  $ hg ci -m 'c_ROOT'
  $ echo a > A
  $ hg add A
  $ hg ci -m 'c_A0'
  $ echo a > B
  $ hg add B
  $ hg ci -m 'c_B0'
  $ hg log -G
  @  changeset:   2:7e594302a05d
  |  tag:         tip
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_B0
  |
  o  changeset:   1:579f120ba918
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_A0
  |
  o  changeset:   0:eba9c2249fe7
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     c_ROOT
  

  $ cd ..

Test rewinding to single changesets
====================================

  $ hg clone rewind-testing-base rewind-testing-simple-prune
  updating to branch default
  3 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ cd rewind-testing-simple-prune

Prune changeset unrelated to the working copy
---------------------------------------------

Setup
`````

Update to an unrelated changeset

  $ hg up 'desc("c_ROOT")'
  0 files updated, 0 files merged, 2 files removed, 0 files unresolved

Prune the head

  $ hg prune -r 'desc("c_B0")'
  1 changesets pruned
  $ hg log -G
  o  changeset:   1:579f120ba918
  |  tag:         tip
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_A0
  |
  @  changeset:   0:eba9c2249fe7
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     c_ROOT
  

Actual rewind
`````````````

  $ hg rewind --hidden --to 'desc("c_B0")'
  rewinded to 1 changesets
  $ hg debugobsolete
  7e594302a05d3769b27be88fc3cdfd39d7498498 0 {579f120ba91885449adc92eedf48ef3569742cee} (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '0', 'operation': 'prune', 'user': 'test'}
  7e594302a05d3769b27be88fc3cdfd39d7498498 073989a581cf430a844192364fa37606357cbbc2 4 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '2', 'operation': 'rewind', 'user': 'test'}
  $ hg obslog -r 'desc("c_B0")'
  o  073989a581cf (3) c_B0
  |
  x  7e594302a05d (2) c_B0
       pruned using prune by test (Thu Jan 01 00:00:00 1970 +0000)
       rewritten(meta) as 073989a581cf using rewind by test (Thu Jan 01 00:00:00 1970 +0000)
  
  $ hg log -G
  o  changeset:   3:073989a581cf
  |  tag:         tip
  |  parent:      1:579f120ba918
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_B0
  |
  o  changeset:   1:579f120ba918
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_A0
  |
  @  changeset:   0:eba9c2249fe7
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     c_ROOT
  
XXX-TODO: fix the obsfate from "meta-changed as 3" to "identical" or something.

  $ hg log -G --hidden
  o  changeset:   3:073989a581cf
  |  tag:         tip
  |  parent:      1:579f120ba918
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_B0
  |
  | x  changeset:   2:7e594302a05d
  |/   user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    obsolete:    meta-changed using rewind as 3:073989a581cf
  |    summary:     c_B0
  |
  o  changeset:   1:579f120ba918
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_A0
  |
  @  changeset:   0:eba9c2249fe7
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     c_ROOT
  

Other independant rewind create a different revision
----------------------------------------------------------

setup
`````

note: we use "default-date" to make it a "different rewind"

  $ echo '[devel]' >> $HGRCPATH
  $ echo 'default-date = 1 0' >> $HGRCPATH

Actual rewind
`````````````

  $ hg prune 'desc("c_B0")'
  1 changesets pruned
  $ hg rewind --hidden --to 'min(desc("c_B0"))'
  rewinded to 1 changesets
  $ hg debugobsolete
  7e594302a05d3769b27be88fc3cdfd39d7498498 0 {579f120ba91885449adc92eedf48ef3569742cee} (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '0', 'operation': 'prune', 'user': 'test'}
  7e594302a05d3769b27be88fc3cdfd39d7498498 073989a581cf430a844192364fa37606357cbbc2 4 (Thu Jan 01 00:00:00 1970 +0000) {'ef1': '2', 'operation': 'rewind', 'user': 'test'}
  073989a581cf430a844192364fa37606357cbbc2 0 {579f120ba91885449adc92eedf48ef3569742cee} (Thu Jan 01 00:00:01 1970 +0000) {'ef1': '0', 'operation': 'prune', 'user': 'test'}
  7e594302a05d3769b27be88fc3cdfd39d7498498 48acf2c0d9c8961859ce9a913671eb2adc9b057b 4 (Thu Jan 01 00:00:01 1970 +0000) {'ef1': '34', 'operation': 'rewind', 'user': 'test'}
  $ hg obslog -r 'desc("c_B0")' --all
  x  073989a581cf (3) c_B0
  |    pruned using prune by test (Thu Jan 01 00:00:01 1970 +0000)
  |
  | o  48acf2c0d9c8 (4) c_B0
  |/
  x  7e594302a05d (2) c_B0
       pruned using prune by test (Thu Jan 01 00:00:00 1970 +0000)
       rewritten(meta) as 073989a581cf using rewind by test (Thu Jan 01 00:00:00 1970 +0000)
       rewritten(meta, date) as 48acf2c0d9c8 using rewind by test (Thu Jan 01 00:00:01 1970 +0000)
  
  $ hg log -G
  o  changeset:   4:48acf2c0d9c8
  |  tag:         tip
  |  parent:      1:579f120ba918
  |  user:        test
  |  date:        Thu Jan 01 00:00:01 1970 +0000
  |  summary:     c_B0
  |
  o  changeset:   1:579f120ba918
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_A0
  |
  @  changeset:   0:eba9c2249fe7
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     c_ROOT
  
  $ hg log -G --hidden
  o  changeset:   4:48acf2c0d9c8
  |  tag:         tip
  |  parent:      1:579f120ba918
  |  user:        test
  |  date:        Thu Jan 01 00:00:01 1970 +0000
  |  summary:     c_B0
  |
  | x  changeset:   3:073989a581cf
  |/   parent:      1:579f120ba918
  |    user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    obsolete:    pruned using prune
  |    summary:     c_B0
  |
  | x  changeset:   2:7e594302a05d
  |/   user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    obsolete:    rewritten using rewind as 4:48acf2c0d9c8
  |    obsolete:    meta-changed using rewind as 3:073989a581cf
  |    summary:     c_B0
  |
  o  changeset:   1:579f120ba918
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_A0
  |
  @  changeset:   0:eba9c2249fe7
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     c_ROOT
  
  $ cd ..

rewind a simple amend - creating content-divergence
---------------------------------------------------

Setup
`````

  $ hg clone rewind-testing-base rewind-testing-single-rewrite
  updating to branch default
  3 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ cd rewind-testing-single-rewrite
  $ echo BB > B
  $ hg amend -m 'c_B1'
  $ hg log -G
  @  changeset:   3:25c8f5ab0c3b
  |  tag:         tip
  |  parent:      1:579f120ba918
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_B1
  |
  o  changeset:   1:579f120ba918
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_A0
  |
  o  changeset:   0:eba9c2249fe7
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     c_ROOT
  

Actual rewind
`````````````

  $ hg rewind --hidden --to 'desc("c_B0")' --as-divergence
  2 new content-divergent changesets
  rewinded to 1 changesets
  $ hg debugobsolete
  7e594302a05d3769b27be88fc3cdfd39d7498498 25c8f5ab0c3bb569ec672570f1a901be4c6f032b 0 (Thu Jan 01 00:00:01 1970 +0000) {'ef1': '9', 'operation': 'amend', 'user': 'test'}
  7e594302a05d3769b27be88fc3cdfd39d7498498 48acf2c0d9c8961859ce9a913671eb2adc9b057b 4 (Thu Jan 01 00:00:01 1970 +0000) {'ef1': '34', 'operation': 'rewind', 'user': 'test'}
  $ hg obslog --rev 'desc("c_B0")'
  *  48acf2c0d9c8 (4) c_B0
  |
  x  7e594302a05d (2) c_B0
       rewritten(description, content) as 25c8f5ab0c3b using amend by test (Thu Jan 01 00:00:01 1970 +0000)
       rewritten(meta, date) as 48acf2c0d9c8 using rewind by test (Thu Jan 01 00:00:01 1970 +0000)
  
  $ hg log -G
  *  changeset:   4:48acf2c0d9c8
  |  tag:         tip
  |  parent:      1:579f120ba918
  |  user:        test
  |  date:        Thu Jan 01 00:00:01 1970 +0000
  |  instability: content-divergent
  |  summary:     c_B0
  |
  | @  changeset:   3:25c8f5ab0c3b
  |/   parent:      1:579f120ba918
  |    user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    instability: content-divergent
  |    summary:     c_B1
  |
  o  changeset:   1:579f120ba918
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_A0
  |
  o  changeset:   0:eba9c2249fe7
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     c_ROOT
  
  $ hg log -G --hidden
  *  changeset:   4:48acf2c0d9c8
  |  tag:         tip
  |  parent:      1:579f120ba918
  |  user:        test
  |  date:        Thu Jan 01 00:00:01 1970 +0000
  |  instability: content-divergent
  |  summary:     c_B0
  |
  | @  changeset:   3:25c8f5ab0c3b
  |/   parent:      1:579f120ba918
  |    user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    instability: content-divergent
  |    summary:     c_B1
  |
  | x  changeset:   2:7e594302a05d
  |/   user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    obsolete:    rewritten using rewind as 4:48acf2c0d9c8
  |    obsolete:    rewritten using amend as 3:25c8f5ab0c3b
  |    summary:     c_B0
  |
  o  changeset:   1:579f120ba918
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_A0
  |
  o  changeset:   0:eba9c2249fe7
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     c_ROOT
  

Cleanup
```````
  $ hg prune 'max(desc("c_B0"))'
  1 changesets pruned
  $ hg log -G
  @  changeset:   3:25c8f5ab0c3b
  |  tag:         tip
  |  parent:      1:579f120ba918
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_B1
  |
  o  changeset:   1:579f120ba918
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_A0
  |
  o  changeset:   0:eba9c2249fe7
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     c_ROOT
  
  $ echo 'default-date = 2 0' >> $HGRCPATH

rewind a simple amend - obsoleting the current latest successors
----------------------------------------------------------------

  $ hg rewind --hidden --to 'min(desc("c_B0"))'
  rewinded to 1 changesets
  (1 changesets obsoleted)
  working directory is now at d8b4471cfb3c
  $ hg debugobsolete
  7e594302a05d3769b27be88fc3cdfd39d7498498 25c8f5ab0c3bb569ec672570f1a901be4c6f032b 0 (Thu Jan 01 00:00:01 1970 +0000) {'ef1': '9', 'operation': 'amend', 'user': 'test'}
  7e594302a05d3769b27be88fc3cdfd39d7498498 48acf2c0d9c8961859ce9a913671eb2adc9b057b 4 (Thu Jan 01 00:00:01 1970 +0000) {'ef1': '34', 'operation': 'rewind', 'user': 'test'}
  48acf2c0d9c8961859ce9a913671eb2adc9b057b 0 {579f120ba91885449adc92eedf48ef3569742cee} (Thu Jan 01 00:00:01 1970 +0000) {'ef1': '0', 'operation': 'prune', 'user': 'test'}
  7e594302a05d3769b27be88fc3cdfd39d7498498 d8b4471cfb3caa290e0a78ae6bc57d78656c9075 4 (Thu Jan 01 00:00:02 1970 +0000) {'ef1': '34', 'operation': 'rewind', 'user': 'test'}
  25c8f5ab0c3bb569ec672570f1a901be4c6f032b d8b4471cfb3caa290e0a78ae6bc57d78656c9075 0 (Thu Jan 01 00:00:02 1970 +0000) {'ef1': '43', 'operation': 'rewind', 'user': 'test'}
  $ hg obslog --rev 'desc("c_B0")'
  @    d8b4471cfb3c (5) c_B0
  |\
  x |  25c8f5ab0c3b (3) c_B1
  |/     rewritten(description, meta, date, content) as d8b4471cfb3c using rewind by test (Thu Jan 01 00:00:02 1970 +0000)
  |
  x  7e594302a05d (2) c_B0
       rewritten(description, content) as 25c8f5ab0c3b using amend by test (Thu Jan 01 00:00:01 1970 +0000)
       rewritten(meta, date) as 48acf2c0d9c8 using rewind by test (Thu Jan 01 00:00:01 1970 +0000)
       rewritten(meta, date) as d8b4471cfb3c using rewind by test (Thu Jan 01 00:00:02 1970 +0000)
  
  $ hg log -G
  @  changeset:   5:d8b4471cfb3c
  |  tag:         tip
  |  parent:      1:579f120ba918
  |  user:        test
  |  date:        Thu Jan 01 00:00:02 1970 +0000
  |  summary:     c_B0
  |
  o  changeset:   1:579f120ba918
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_A0
  |
  o  changeset:   0:eba9c2249fe7
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     c_ROOT
  
  $ hg log -G --hidden
  @  changeset:   5:d8b4471cfb3c
  |  tag:         tip
  |  parent:      1:579f120ba918
  |  user:        test
  |  date:        Thu Jan 01 00:00:02 1970 +0000
  |  summary:     c_B0
  |
  | x  changeset:   4:48acf2c0d9c8
  |/   parent:      1:579f120ba918
  |    user:        test
  |    date:        Thu Jan 01 00:00:01 1970 +0000
  |    obsolete:    pruned using prune
  |    summary:     c_B0
  |
  | x  changeset:   3:25c8f5ab0c3b
  |/   parent:      1:579f120ba918
  |    user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    obsolete:    rewritten using rewind as 5:d8b4471cfb3c
  |    summary:     c_B1
  |
  | x  changeset:   2:7e594302a05d
  |/   user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    obsolete:    rewritten using rewind as 5:d8b4471cfb3c
  |    obsolete:    rewritten using rewind as 4:48acf2c0d9c8
  |    obsolete:    rewritten using amend as 3:25c8f5ab0c3b
  |    summary:     c_B0
  |
  o  changeset:   1:579f120ba918
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_A0
  |
  o  changeset:   0:eba9c2249fe7
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     c_ROOT
  
  $ cd ..

rewind a simple split
---------------------

Setup
`````

  $ hg clone rewind-testing-base rewind-testing-split-fold
  updating to branch default
  3 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ cd rewind-testing-split-fold

  $ echo C > C
  $ echo D > D
  $ hg add C D
  $ hg ci -m 'c_CD0'
  $ hg split << EOF
  > y
  > f
  > d
  > y
  > EOF
  0 files updated, 0 files merged, 2 files removed, 0 files unresolved
  adding C
  adding D
  diff --git a/C b/C
  new file mode 100644
  examine changes to 'C'? [Ynesfdaq?] y
  
  @@ -0,0 +1,1 @@
  +C
  record change 1/2 to 'C'? [Ynesfdaq?] f
  
  diff --git a/D b/D
  new file mode 100644
  examine changes to 'D'? [Ynesfdaq?] d
  
  created new head
  Done splitting? [yN] y
  $ hg log -G
  @  changeset:   5:9576e80d6851
  |  tag:         tip
  |  user:        test
  |  date:        Thu Jan 01 00:00:02 1970 +0000
  |  summary:     c_CD0
  |
  o  changeset:   4:a0316c4c5417
  |  parent:      2:7e594302a05d
  |  user:        test
  |  date:        Thu Jan 01 00:00:02 1970 +0000
  |  summary:     c_CD0
  |
  o  changeset:   2:7e594302a05d
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_B0
  |
  o  changeset:   1:579f120ba918
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_A0
  |
  o  changeset:   0:eba9c2249fe7
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     c_ROOT
  
  $ hg debugobsolete
  49fb7d900906b0a3d329e90da4dcb0a7582d3b6e a0316c4c54179357e71d068fb8884678ebc7c351 9576e80d6851ce79cd535e2dc5fa01b444d89a39 0 (Thu Jan 01 00:00:02 1970 +0000) {'ef1': '12', 'operation': 'split', 'user': 'test'}
  $ hg obslog --all
  @  9576e80d6851 (5) c_CD0
  |
  | o  a0316c4c5417 (4) c_CD0
  |/
  x  49fb7d900906 (3) c_CD0
       rewritten(parent, content) as 9576e80d6851, a0316c4c5417 using split by test (Thu Jan 01 00:00:02 1970 +0000)
  

Actual rewind
`````````````

  $ hg rewind --hidden --to 'min(desc("c_CD0"))'
  rewinded to 1 changesets
  (2 changesets obsoleted)
  working directory is now at 4535d0af405c
  $ hg debugobsolete
  49fb7d900906b0a3d329e90da4dcb0a7582d3b6e a0316c4c54179357e71d068fb8884678ebc7c351 9576e80d6851ce79cd535e2dc5fa01b444d89a39 0 (Thu Jan 01 00:00:02 1970 +0000) {'ef1': '12', 'operation': 'split', 'user': 'test'}
  49fb7d900906b0a3d329e90da4dcb0a7582d3b6e 4535d0af405c1bf35f37b35f26ec6f9acfa6fe0b 4 (Thu Jan 01 00:00:02 1970 +0000) {'ef1': '2', 'operation': 'rewind', 'user': 'test'}
  9576e80d6851ce79cd535e2dc5fa01b444d89a39 4535d0af405c1bf35f37b35f26ec6f9acfa6fe0b 0 (Thu Jan 01 00:00:02 1970 +0000) {'ef1': '14', 'operation': 'rewind', 'user': 'test'}
  a0316c4c54179357e71d068fb8884678ebc7c351 4535d0af405c1bf35f37b35f26ec6f9acfa6fe0b 0 (Thu Jan 01 00:00:02 1970 +0000) {'ef1': '10', 'operation': 'rewind', 'user': 'test'}
  $ hg obslog
  @    4535d0af405c (6) c_CD0
  |\
  | \
  | |\
  | x |  9576e80d6851 (5) c_CD0
  |/ /     rewritten(meta, parent, content) as 4535d0af405c using rewind by test (Thu Jan 01 00:00:02 1970 +0000)
  | |
  | x  a0316c4c5417 (4) c_CD0
  |/     rewritten(meta, content) as 4535d0af405c using rewind by test (Thu Jan 01 00:00:02 1970 +0000)
  |
  x  49fb7d900906 (3) c_CD0
       rewritten(meta) as 4535d0af405c using rewind by test (Thu Jan 01 00:00:02 1970 +0000)
       rewritten(parent, content) as 9576e80d6851, a0316c4c5417 using split by test (Thu Jan 01 00:00:02 1970 +0000)
  
  $ hg log -G
  @  changeset:   6:4535d0af405c
  |  tag:         tip
  |  parent:      2:7e594302a05d
  |  user:        test
  |  date:        Thu Jan 01 00:00:02 1970 +0000
  |  summary:     c_CD0
  |
  o  changeset:   2:7e594302a05d
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_B0
  |
  o  changeset:   1:579f120ba918
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_A0
  |
  o  changeset:   0:eba9c2249fe7
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     c_ROOT
  

rewind a fold
-------------

setup
`````

  $ echo 'default-date = 3 0' >> $HGRCPATH

Actual Rewind
`````````````

  $ hg rewind --to '9576e80d6851+a0316c4c5417' --hidden
  rewinded to 2 changesets
  (1 changesets obsoleted)
  working directory is now at 85be7b94f69e
  $ hg debugobsolete
  49fb7d900906b0a3d329e90da4dcb0a7582d3b6e a0316c4c54179357e71d068fb8884678ebc7c351 9576e80d6851ce79cd535e2dc5fa01b444d89a39 0 (Thu Jan 01 00:00:02 1970 +0000) {'ef1': '12', 'operation': 'split', 'user': 'test'}
  49fb7d900906b0a3d329e90da4dcb0a7582d3b6e 4535d0af405c1bf35f37b35f26ec6f9acfa6fe0b 4 (Thu Jan 01 00:00:02 1970 +0000) {'ef1': '2', 'operation': 'rewind', 'user': 'test'}
  9576e80d6851ce79cd535e2dc5fa01b444d89a39 4535d0af405c1bf35f37b35f26ec6f9acfa6fe0b 0 (Thu Jan 01 00:00:02 1970 +0000) {'ef1': '14', 'operation': 'rewind', 'user': 'test'}
  a0316c4c54179357e71d068fb8884678ebc7c351 4535d0af405c1bf35f37b35f26ec6f9acfa6fe0b 0 (Thu Jan 01 00:00:02 1970 +0000) {'ef1': '10', 'operation': 'rewind', 'user': 'test'}
  a0316c4c54179357e71d068fb8884678ebc7c351 73a1ac2e570de1f33bbea7d8260b00d5af1d30a7 4 (Thu Jan 01 00:00:03 1970 +0000) {'ef1': '34', 'operation': 'rewind', 'user': 'test'}
  9576e80d6851ce79cd535e2dc5fa01b444d89a39 85be7b94f69e936d6f0fc52118211da82fe4e838 4 (Thu Jan 01 00:00:03 1970 +0000) {'ef1': '38', 'operation': 'rewind', 'user': 'test'}
  4535d0af405c1bf35f37b35f26ec6f9acfa6fe0b 73a1ac2e570de1f33bbea7d8260b00d5af1d30a7 85be7b94f69e936d6f0fc52118211da82fe4e838 0 (Thu Jan 01 00:00:03 1970 +0000) {'ef1': '46', 'operation': 'rewind', 'user': 'test'}
  $ hg obslog -r -2:
  o    73a1ac2e570d (7) c_CD0
  |\
  +---@  85be7b94f69e (8) c_CD0
  | | |
  x---+  4535d0af405c (6) c_CD0
  |\| |    rewritten(meta, date, parent, content) as 73a1ac2e570d, 85be7b94f69e using rewind by test (Thu Jan 01 00:00:03 1970 +0000)
  | | |
  +---x  9576e80d6851 (5) c_CD0
  | |      rewritten(meta, parent, content) as 4535d0af405c using rewind by test (Thu Jan 01 00:00:02 1970 +0000)
  | |      rewritten(meta, date, parent) as 85be7b94f69e using rewind by test (Thu Jan 01 00:00:03 1970 +0000)
  | |
  | x  a0316c4c5417 (4) c_CD0
  |/     rewritten(meta, content) as 4535d0af405c using rewind by test (Thu Jan 01 00:00:02 1970 +0000)
  |      rewritten(meta, date) as 73a1ac2e570d using rewind by test (Thu Jan 01 00:00:03 1970 +0000)
  |
  x  49fb7d900906 (3) c_CD0
       rewritten(meta) as 4535d0af405c using rewind by test (Thu Jan 01 00:00:02 1970 +0000)
       rewritten(parent, content) as 9576e80d6851, a0316c4c5417 using split by test (Thu Jan 01 00:00:02 1970 +0000)
  
  $ hg log -G
  @  changeset:   8:85be7b94f69e
  |  tag:         tip
  |  user:        test
  |  date:        Thu Jan 01 00:00:03 1970 +0000
  |  summary:     c_CD0
  |
  o  changeset:   7:73a1ac2e570d
  |  parent:      2:7e594302a05d
  |  user:        test
  |  date:        Thu Jan 01 00:00:03 1970 +0000
  |  summary:     c_CD0
  |
  o  changeset:   2:7e594302a05d
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_B0
  |
  o  changeset:   1:579f120ba918
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_A0
  |
  o  changeset:   0:eba9c2249fe7
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     c_ROOT
  
  $ cd ..

Test rewinding stack
====================

  $ hg clone rewind-testing-base rewind-testing-stack
  updating to branch default
  3 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ cd rewind-testing-stack

Rewinding the top of the stack only
-----------------------------------

setup
`````

  $ hg up 'desc("c_A0")'
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ echo AA >> A
  $ hg amend -m 'c_A1'
  1 new orphan changesets
  $ hg evolve --all
  move:[2] c_B0
  atop:[3] c_A1
  working directory is now at a65fceb2324a
  $ hg debugobsolete
  579f120ba91885449adc92eedf48ef3569742cee d952d1794ff657f5c2a82225d2e6307ed930b32f 0 (Thu Jan 01 00:00:03 1970 +0000) {'ef1': '9', 'operation': 'amend', 'user': 'test'}
  7e594302a05d3769b27be88fc3cdfd39d7498498 a65fceb2324ae1eb1231610193d24a5fa02c7c0e 0 (Thu Jan 01 00:00:03 1970 +0000) {'ef1': '4', 'operation': 'evolve', 'user': 'test'}
  $ hg obslog -r 'desc("c_A1")::'
  @  a65fceb2324a (4) c_B0
  |
  | o  d952d1794ff6 (3) c_A1
  | |
  | x  579f120ba918 (1) c_A0
  |      rewritten(description, content) as d952d1794ff6 using amend by test (Thu Jan 01 00:00:03 1970 +0000)
  |
  x  7e594302a05d (2) c_B0
       rewritten(parent) as a65fceb2324a using evolve by test (Thu Jan 01 00:00:03 1970 +0000)
  
  $ hg log -G
  @  changeset:   4:a65fceb2324a
  |  tag:         tip
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_B0
  |
  o  changeset:   3:d952d1794ff6
  |  parent:      0:eba9c2249fe7
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_A1
  |
  o  changeset:   0:eba9c2249fe7
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     c_ROOT
  

Actual rewind
`````````````

  $ hg rewind --hidden --to 'min(desc(c_B0))' --exact
  1 new orphan changesets
  rewinded to 1 changesets
  (1 changesets obsoleted)
  working directory is now at 96622b0702dd
  $ hg debugobsolete
  579f120ba91885449adc92eedf48ef3569742cee d952d1794ff657f5c2a82225d2e6307ed930b32f 0 (Thu Jan 01 00:00:03 1970 +0000) {'ef1': '9', 'operation': 'amend', 'user': 'test'}
  7e594302a05d3769b27be88fc3cdfd39d7498498 a65fceb2324ae1eb1231610193d24a5fa02c7c0e 0 (Thu Jan 01 00:00:03 1970 +0000) {'ef1': '4', 'operation': 'evolve', 'user': 'test'}
  7e594302a05d3769b27be88fc3cdfd39d7498498 96622b0702dd86e3a702b0235b420da41f072efe 4 (Thu Jan 01 00:00:03 1970 +0000) {'ef1': '34', 'operation': 'rewind', 'user': 'test'}
  a65fceb2324ae1eb1231610193d24a5fa02c7c0e 96622b0702dd86e3a702b0235b420da41f072efe 0 (Thu Jan 01 00:00:03 1970 +0000) {'ef1': '38', 'operation': 'rewind', 'user': 'test'}
  $ hg obslog
  @    96622b0702dd (5) c_B0
  |\
  | x  a65fceb2324a (4) c_B0
  |/     rewritten(meta, date, parent) as 96622b0702dd using rewind by test (Thu Jan 01 00:00:03 1970 +0000)
  |
  x  7e594302a05d (2) c_B0
       rewritten(meta, date) as 96622b0702dd using rewind by test (Thu Jan 01 00:00:03 1970 +0000)
       rewritten(parent) as a65fceb2324a using evolve by test (Thu Jan 01 00:00:03 1970 +0000)
  
  $ hg log -G
  @  changeset:   5:96622b0702dd
  |  tag:         tip
  |  parent:      1:579f120ba918
  |  user:        test
  |  date:        Thu Jan 01 00:00:03 1970 +0000
  |  instability: orphan
  |  summary:     c_B0
  |
  | o  changeset:   3:d952d1794ff6
  | |  parent:      0:eba9c2249fe7
  | |  user:        test
  | |  date:        Thu Jan 01 00:00:00 1970 +0000
  | |  summary:     c_A1
  | |
  x |  changeset:   1:579f120ba918
  |/   user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    obsolete:    rewritten using amend as 3:d952d1794ff6
  |    summary:     c_A0
  |
  o  changeset:   0:eba9c2249fe7
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     c_ROOT
  

Testing default argument (and cleanup)
``````````````````````````````````````

rewind with no argument should be equivalent to `--from .`

  $ echo 'default-date = 4 0' >> $HGRCPATH
  $ hg rewind --from '.'
  rewinded to 1 changesets
  (1 changesets obsoleted)
  working directory is now at 7b1440274cc3
  $ echo 'default-date = 5 0' >> $HGRCPATH
  $ hg log -G
  @  changeset:   6:7b1440274cc3
  |  tag:         tip
  |  parent:      3:d952d1794ff6
  |  user:        test
  |  date:        Thu Jan 01 00:00:04 1970 +0000
  |  summary:     c_B0
  |
  o  changeset:   3:d952d1794ff6
  |  parent:      0:eba9c2249fe7
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_A1
  |
  o  changeset:   0:eba9c2249fe7
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     c_ROOT
  
  $ hg debugobsolete
  579f120ba91885449adc92eedf48ef3569742cee d952d1794ff657f5c2a82225d2e6307ed930b32f 0 (Thu Jan 01 00:00:03 1970 +0000) {'ef1': '9', 'operation': 'amend', 'user': 'test'}
  7e594302a05d3769b27be88fc3cdfd39d7498498 a65fceb2324ae1eb1231610193d24a5fa02c7c0e 0 (Thu Jan 01 00:00:03 1970 +0000) {'ef1': '4', 'operation': 'evolve', 'user': 'test'}
  7e594302a05d3769b27be88fc3cdfd39d7498498 96622b0702dd86e3a702b0235b420da41f072efe 4 (Thu Jan 01 00:00:03 1970 +0000) {'ef1': '34', 'operation': 'rewind', 'user': 'test'}
  a65fceb2324ae1eb1231610193d24a5fa02c7c0e 96622b0702dd86e3a702b0235b420da41f072efe 0 (Thu Jan 01 00:00:03 1970 +0000) {'ef1': '38', 'operation': 'rewind', 'user': 'test'}
  a65fceb2324ae1eb1231610193d24a5fa02c7c0e 7b1440274cc3b3f8bfcffc891172a7d2d7e9140c 4 (Thu Jan 01 00:00:04 1970 +0000) {'ef1': '34', 'operation': 'rewind', 'user': 'test'}
  96622b0702dd86e3a702b0235b420da41f072efe 7b1440274cc3b3f8bfcffc891172a7d2d7e9140c 0 (Thu Jan 01 00:00:04 1970 +0000) {'ef1': '38', 'operation': 'rewind', 'user': 'test'}
  $ hg obslog
  @    7b1440274cc3 (6) c_B0
  |\
  x |  96622b0702dd (5) c_B0
  |\|    rewritten(meta, date, parent) as 7b1440274cc3 using rewind by test (Thu Jan 01 00:00:04 1970 +0000)
  | |
  | x  a65fceb2324a (4) c_B0
  |/     rewritten(meta, date) as 7b1440274cc3 using rewind by test (Thu Jan 01 00:00:04 1970 +0000)
  |      rewritten(meta, date, parent) as 96622b0702dd using rewind by test (Thu Jan 01 00:00:03 1970 +0000)
  |
  x  7e594302a05d (2) c_B0
       rewritten(meta, date) as 96622b0702dd using rewind by test (Thu Jan 01 00:00:03 1970 +0000)
       rewritten(parent) as a65fceb2324a using evolve by test (Thu Jan 01 00:00:03 1970 +0000)
  
Automatically rewinding the full stack (with --to)
--------------------------------------------------

  $ hg rewind --hidden --to 'precursors(.)'
  rewinded to 2 changesets
  (2 changesets obsoleted)
  working directory is now at 70892f498f29
  $ hg debugobsolete
  579f120ba91885449adc92eedf48ef3569742cee d952d1794ff657f5c2a82225d2e6307ed930b32f 0 (Thu Jan 01 00:00:03 1970 +0000) {'ef1': '9', 'operation': 'amend', 'user': 'test'}
  7e594302a05d3769b27be88fc3cdfd39d7498498 a65fceb2324ae1eb1231610193d24a5fa02c7c0e 0 (Thu Jan 01 00:00:03 1970 +0000) {'ef1': '4', 'operation': 'evolve', 'user': 'test'}
  7e594302a05d3769b27be88fc3cdfd39d7498498 96622b0702dd86e3a702b0235b420da41f072efe 4 (Thu Jan 01 00:00:03 1970 +0000) {'ef1': '34', 'operation': 'rewind', 'user': 'test'}
  a65fceb2324ae1eb1231610193d24a5fa02c7c0e 96622b0702dd86e3a702b0235b420da41f072efe 0 (Thu Jan 01 00:00:03 1970 +0000) {'ef1': '38', 'operation': 'rewind', 'user': 'test'}
  a65fceb2324ae1eb1231610193d24a5fa02c7c0e 7b1440274cc3b3f8bfcffc891172a7d2d7e9140c 4 (Thu Jan 01 00:00:04 1970 +0000) {'ef1': '34', 'operation': 'rewind', 'user': 'test'}
  96622b0702dd86e3a702b0235b420da41f072efe 7b1440274cc3b3f8bfcffc891172a7d2d7e9140c 0 (Thu Jan 01 00:00:04 1970 +0000) {'ef1': '38', 'operation': 'rewind', 'user': 'test'}
  579f120ba91885449adc92eedf48ef3569742cee c0d232501dd8e52b8ca8a266f25db89f5120c17f 4 (Thu Jan 01 00:00:05 1970 +0000) {'ef1': '34', 'operation': 'rewind', 'user': 'test'}
  96622b0702dd86e3a702b0235b420da41f072efe 70892f498f2993d626848bb312ff856168d0b9c4 4 (Thu Jan 01 00:00:05 1970 +0000) {'ef1': '38', 'operation': 'rewind', 'user': 'test'}
  7b1440274cc3b3f8bfcffc891172a7d2d7e9140c 70892f498f2993d626848bb312ff856168d0b9c4 0 (Thu Jan 01 00:00:05 1970 +0000) {'ef1': '38', 'operation': 'rewind', 'user': 'test'}
  d952d1794ff657f5c2a82225d2e6307ed930b32f c0d232501dd8e52b8ca8a266f25db89f5120c17f 0 (Thu Jan 01 00:00:05 1970 +0000) {'ef1': '43', 'operation': 'rewind', 'user': 'test'}
  $ hg obslog
  @    70892f498f29 (8) c_B0
  |\
  x |  7b1440274cc3 (6) c_B0
  |\|    rewritten(meta, date, parent) as 70892f498f29 using rewind by test (Thu Jan 01 00:00:05 1970 +0000)
  | |
  | x  96622b0702dd (5) c_B0
  |/|    rewritten(meta, date, parent) as 70892f498f29 using rewind by test (Thu Jan 01 00:00:05 1970 +0000)
  | |    rewritten(meta, date, parent) as 7b1440274cc3 using rewind by test (Thu Jan 01 00:00:04 1970 +0000)
  | |
  x |  a65fceb2324a (4) c_B0
  |/     rewritten(meta, date) as 7b1440274cc3 using rewind by test (Thu Jan 01 00:00:04 1970 +0000)
  |      rewritten(meta, date, parent) as 96622b0702dd using rewind by test (Thu Jan 01 00:00:03 1970 +0000)
  |
  x  7e594302a05d (2) c_B0
       rewritten(meta, date) as 96622b0702dd using rewind by test (Thu Jan 01 00:00:03 1970 +0000)
       rewritten(parent) as a65fceb2324a using evolve by test (Thu Jan 01 00:00:03 1970 +0000)
  
  $ hg log -G
  @  changeset:   8:70892f498f29
  |  tag:         tip
  |  user:        test
  |  date:        Thu Jan 01 00:00:05 1970 +0000
  |  summary:     c_B0
  |
  o  changeset:   7:c0d232501dd8
  |  parent:      0:eba9c2249fe7
  |  user:        test
  |  date:        Thu Jan 01 00:00:05 1970 +0000
  |  summary:     c_A0
  |
  o  changeset:   0:eba9c2249fe7
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     c_ROOT
  

Automatically rewinding the full stack (with --from)
----------------------------------------------------

  $ echo 'default-date = 6 0' >> $HGRCPATH
  $ hg rewind --hidden --from '.'
  rewinded to 2 changesets
  (2 changesets obsoleted)
  working directory is now at 141aedbbde8f
  $ hg debugobsolete
  579f120ba91885449adc92eedf48ef3569742cee d952d1794ff657f5c2a82225d2e6307ed930b32f 0 (Thu Jan 01 00:00:03 1970 +0000) {'ef1': '9', 'operation': 'amend', 'user': 'test'}
  7e594302a05d3769b27be88fc3cdfd39d7498498 a65fceb2324ae1eb1231610193d24a5fa02c7c0e 0 (Thu Jan 01 00:00:03 1970 +0000) {'ef1': '4', 'operation': 'evolve', 'user': 'test'}
  7e594302a05d3769b27be88fc3cdfd39d7498498 96622b0702dd86e3a702b0235b420da41f072efe 4 (Thu Jan 01 00:00:03 1970 +0000) {'ef1': '34', 'operation': 'rewind', 'user': 'test'}
  a65fceb2324ae1eb1231610193d24a5fa02c7c0e 96622b0702dd86e3a702b0235b420da41f072efe 0 (Thu Jan 01 00:00:03 1970 +0000) {'ef1': '38', 'operation': 'rewind', 'user': 'test'}
  a65fceb2324ae1eb1231610193d24a5fa02c7c0e 7b1440274cc3b3f8bfcffc891172a7d2d7e9140c 4 (Thu Jan 01 00:00:04 1970 +0000) {'ef1': '34', 'operation': 'rewind', 'user': 'test'}
  96622b0702dd86e3a702b0235b420da41f072efe 7b1440274cc3b3f8bfcffc891172a7d2d7e9140c 0 (Thu Jan 01 00:00:04 1970 +0000) {'ef1': '38', 'operation': 'rewind', 'user': 'test'}
  579f120ba91885449adc92eedf48ef3569742cee c0d232501dd8e52b8ca8a266f25db89f5120c17f 4 (Thu Jan 01 00:00:05 1970 +0000) {'ef1': '34', 'operation': 'rewind', 'user': 'test'}
  96622b0702dd86e3a702b0235b420da41f072efe 70892f498f2993d626848bb312ff856168d0b9c4 4 (Thu Jan 01 00:00:05 1970 +0000) {'ef1': '38', 'operation': 'rewind', 'user': 'test'}
  7b1440274cc3b3f8bfcffc891172a7d2d7e9140c 70892f498f2993d626848bb312ff856168d0b9c4 0 (Thu Jan 01 00:00:05 1970 +0000) {'ef1': '38', 'operation': 'rewind', 'user': 'test'}
  d952d1794ff657f5c2a82225d2e6307ed930b32f c0d232501dd8e52b8ca8a266f25db89f5120c17f 0 (Thu Jan 01 00:00:05 1970 +0000) {'ef1': '43', 'operation': 'rewind', 'user': 'test'}
  d952d1794ff657f5c2a82225d2e6307ed930b32f 7b4aed5e99d2734da6cc25f0095876c5cb6e8084 4 (Thu Jan 01 00:00:06 1970 +0000) {'ef1': '34', 'operation': 'rewind', 'user': 'test'}
  7b1440274cc3b3f8bfcffc891172a7d2d7e9140c 141aedbbde8f407fc8a8a7355221733b0fc01ca5 4 (Thu Jan 01 00:00:06 1970 +0000) {'ef1': '38', 'operation': 'rewind', 'user': 'test'}
  70892f498f2993d626848bb312ff856168d0b9c4 141aedbbde8f407fc8a8a7355221733b0fc01ca5 0 (Thu Jan 01 00:00:06 1970 +0000) {'ef1': '38', 'operation': 'rewind', 'user': 'test'}
  c0d232501dd8e52b8ca8a266f25db89f5120c17f 7b4aed5e99d2734da6cc25f0095876c5cb6e8084 0 (Thu Jan 01 00:00:06 1970 +0000) {'ef1': '43', 'operation': 'rewind', 'user': 'test'}
  $ hg obslog
  @    141aedbbde8f (10) c_B0
  |\
  x |  70892f498f29 (8) c_B0
  |\|    rewritten(meta, date, parent) as 141aedbbde8f using rewind by test (Thu Jan 01 00:00:06 1970 +0000)
  | |
  | x  7b1440274cc3 (6) c_B0
  |/|    rewritten(meta, date, parent) as 141aedbbde8f using rewind by test (Thu Jan 01 00:00:06 1970 +0000)
  | |    rewritten(meta, date, parent) as 70892f498f29 using rewind by test (Thu Jan 01 00:00:05 1970 +0000)
  | |
  x |  96622b0702dd (5) c_B0
  |\|    rewritten(meta, date, parent) as 70892f498f29 using rewind by test (Thu Jan 01 00:00:05 1970 +0000)
  | |    rewritten(meta, date, parent) as 7b1440274cc3 using rewind by test (Thu Jan 01 00:00:04 1970 +0000)
  | |
  | x  a65fceb2324a (4) c_B0
  |/     rewritten(meta, date) as 7b1440274cc3 using rewind by test (Thu Jan 01 00:00:04 1970 +0000)
  |      rewritten(meta, date, parent) as 96622b0702dd using rewind by test (Thu Jan 01 00:00:03 1970 +0000)
  |
  x  7e594302a05d (2) c_B0
       rewritten(meta, date) as 96622b0702dd using rewind by test (Thu Jan 01 00:00:03 1970 +0000)
       rewritten(parent) as a65fceb2324a using evolve by test (Thu Jan 01 00:00:03 1970 +0000)
  
  $ hg log -G
  @  changeset:   10:141aedbbde8f
  |  tag:         tip
  |  user:        test
  |  date:        Thu Jan 01 00:00:06 1970 +0000
  |  summary:     c_B0
  |
  o  changeset:   9:7b4aed5e99d2
  |  parent:      0:eba9c2249fe7
  |  user:        test
  |  date:        Thu Jan 01 00:00:06 1970 +0000
  |  summary:     c_A1
  |
  o  changeset:   0:eba9c2249fe7
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     c_ROOT
  
  $ cd ..

Check error cases
=================

  $ hg clone rewind-testing-base rewind-testing-error
  updating to branch default
  3 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ cd rewind-testing-error

Uncommited changes
------------------

  $ echo C > C
  $ hg add C
  $ hg rewind
  abort: uncommitted changes
  [255]
