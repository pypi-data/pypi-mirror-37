This test file test the various messages when accessing obsolete
revisions.

Global setup
============

  $ . $TESTDIR/testlib/obshistory_setup.sh

Test output with lots of splitted commit
========================================

Test setup
----------

  $ hg init $TESTTMP/local-lots-split
  $ cd $TESTTMP/local-lots-split
  $ mkcommit ROOT
  $ echo 42 >> a
  $ echo 43 >> b
  $ echo 44 >> c
  $ echo 45 >> d
  $ hg commit -A -m "A0"
  adding a
  adding b
  adding c
  adding d
  $ hg log --hidden -G
  @  changeset:   1:de7290d8b885
  |  tag:         tip
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     A0
  |
  o  changeset:   0:ea207398892e
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     ROOT
  

  $ hg split -r 'desc(A0)' -d "0 0" << EOF
  > y
  > y
  > n
  > n
  > n
  > n
  > y
  > y
  > n
  > n
  > n
  > y
  > y
  > n
  > n
  > y
  > y
  > EOF
  0 files updated, 0 files merged, 4 files removed, 0 files unresolved
  adding a
  adding b
  adding c
  adding d
  diff --git a/a b/a
  new file mode 100644
  examine changes to 'a'? [Ynesfdaq?] y
  
  @@ -0,0 +1,1 @@
  +42
  record change 1/4 to 'a'? [Ynesfdaq?] y
  
  diff --git a/b b/b
  new file mode 100644
  examine changes to 'b'? [Ynesfdaq?] n
  
  diff --git a/c b/c
  new file mode 100644
  examine changes to 'c'? [Ynesfdaq?] n
  
  diff --git a/d b/d
  new file mode 100644
  examine changes to 'd'? [Ynesfdaq?] n
  
  created new head
  Done splitting? [yN] n
  diff --git a/b b/b
  new file mode 100644
  examine changes to 'b'? [Ynesfdaq?] y
  
  @@ -0,0 +1,1 @@
  +43
  record change 1/3 to 'b'? [Ynesfdaq?] y
  
  diff --git a/c b/c
  new file mode 100644
  examine changes to 'c'? [Ynesfdaq?] n
  
  diff --git a/d b/d
  new file mode 100644
  examine changes to 'd'? [Ynesfdaq?] n
  
  Done splitting? [yN] n
  diff --git a/c b/c
  new file mode 100644
  examine changes to 'c'? [Ynesfdaq?] y
  
  @@ -0,0 +1,1 @@
  +44
  record change 1/2 to 'c'? [Ynesfdaq?] y
  
  diff --git a/d b/d
  new file mode 100644
  examine changes to 'd'? [Ynesfdaq?] n
  
  Done splitting? [yN] n
  diff --git a/d b/d
  new file mode 100644
  examine changes to 'd'? [Ynesfdaq?] y
  
  @@ -0,0 +1,1 @@
  +45
  record this change to 'd'? [Ynesfdaq?] y
  
  no more change to split

  $ hg log --hidden -G
  @  changeset:   5:c7f044602e9b
  |  tag:         tip
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     A0
  |
  o  changeset:   4:1ae8bc733a14
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     A0
  |
  o  changeset:   3:f257fde29c7a
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     A0
  |
  o  changeset:   2:337fec4d2edc
  |  parent:      0:ea207398892e
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     A0
  |
  | x  changeset:   1:de7290d8b885
  |/   user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    obsolete:    split using split as 2:337fec4d2edc, 3:f257fde29c7a, 4:1ae8bc733a14, 5:c7f044602e9b
  |    summary:     A0
  |
  o  changeset:   0:ea207398892e
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     ROOT
  
Actual test
-----------

  $ hg obslog de7290d8b885 --hidden --patch
  x  de7290d8b885 (1) A0
       rewritten(parent, content) as 1ae8bc733a14, 337fec4d2edc, c7f044602e9b, f257fde29c7a using split by test (Thu Jan 01 00:00:00 1970 +0000)
         (No patch available, too many successors (4))
  
  $ hg obslog de7290d8b885 --hidden --all --patch
  o  1ae8bc733a14 (4) A0
  |
  | o  337fec4d2edc (2) A0
  |/
  | @  c7f044602e9b (5) A0
  |/
  | o  f257fde29c7a (3) A0
  |/
  x  de7290d8b885 (1) A0
       rewritten(parent, content) as 1ae8bc733a14, 337fec4d2edc, c7f044602e9b, f257fde29c7a using split by test (Thu Jan 01 00:00:00 1970 +0000)
         (No patch available, too many successors (4))
  
  $ hg obslog de7290d8b885 --hidden --no-graph -Tjson | python -m json.tool
  [
      {
          "markers": [
              {
                  "date": [
                      *, (glob)
                      0 (glob)
                  ],
                  "effect": [
                      "parent",
                      "content"
                  ],
                  "operation": "split",
                  "succnodes": [
                      "1ae8bc733a14",
                      "337fec4d2edc",
                      "c7f044602e9b",
                      "f257fde29c7a"
                  ],
                  "user": "test",
                  "verb": "rewritten"
              }
          ],
          "node": "de7290d8b885",
          "rev": 1,
          "shortdescription": "A0"
      }
  ]
  $ hg obslog c7f044602e9b --patch
  @  c7f044602e9b (5) A0
  |
  x  de7290d8b885 (1) A0
       rewritten(parent, content) as 1ae8bc733a14, 337fec4d2edc, c7f044602e9b, f257fde29c7a using split by test (Thu Jan 01 00:00:00 1970 +0000)
         (No patch available, too many successors (4))
  
  $ hg obslog c7f044602e9b --no-graph -Tjson | python -m json.tool
  [
      {
          "markers": [],
          "node": "c7f044602e9b",
          "rev": 5,
          "shortdescription": "A0"
      },
      {
          "markers": [
              {
                  "date": [
                      *, (glob)
                      0 (glob)
                  ],
                  "effect": [
                      "parent",
                      "content"
                  ],
                  "operation": "split",
                  "succnodes": [
                      "1ae8bc733a14",
                      "337fec4d2edc",
                      "c7f044602e9b",
                      "f257fde29c7a"
                  ],
                  "user": "test",
                  "verb": "rewritten"
              }
          ],
          "node": "de7290d8b885",
          "rev": 1,
          "shortdescription": "A0"
      }
  ]
Check that debugobshistory on all heads show a coherent graph
  $ hg obslog 2::5 --patch
  o  1ae8bc733a14 (4) A0
  |
  | o  337fec4d2edc (2) A0
  |/
  | @  c7f044602e9b (5) A0
  |/
  | o  f257fde29c7a (3) A0
  |/
  x  de7290d8b885 (1) A0
       rewritten(parent, content) as 1ae8bc733a14, 337fec4d2edc, c7f044602e9b, f257fde29c7a using split by test (Thu Jan 01 00:00:00 1970 +0000)
         (No patch available, too many successors (4))
  
  $ hg obslog 5 --all --patch
  o  1ae8bc733a14 (4) A0
  |
  | o  337fec4d2edc (2) A0
  |/
  | @  c7f044602e9b (5) A0
  |/
  | o  f257fde29c7a (3) A0
  |/
  x  de7290d8b885 (1) A0
       rewritten(parent, content) as 1ae8bc733a14, 337fec4d2edc, c7f044602e9b, f257fde29c7a using split by test (Thu Jan 01 00:00:00 1970 +0000)
         (No patch available, too many successors (4))
  
  $ hg update de7290d8b885
  abort: hidden revision 'de7290d8b885' was split as: 337fec4d2edc, f257fde29c7a and 2 more!
  (use --hidden to access hidden revisions)
  [255]
  $ hg update --hidden 'min(desc(A0))'
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  updated to hidden changeset de7290d8b885
  (hidden revision 'de7290d8b885' was split as: 337fec4d2edc, f257fde29c7a and 2 more)
  working directory parent is obsolete! (de7290d8b885)
  (use 'hg evolve' to update to its tipmost successor: 337fec4d2edc, f257fde29c7a and 2 more)
