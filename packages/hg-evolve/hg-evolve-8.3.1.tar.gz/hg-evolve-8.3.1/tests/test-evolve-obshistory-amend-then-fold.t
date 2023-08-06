This test file test the various messages when accessing obsolete
revisions.

Global setup
============

  $ . $TESTDIR/testlib/obshistory_setup.sh

Test output with amended + folded commit
========================================

Test setup
----------

  $ hg init $TESTTMP/local-amend-fold
  $ cd $TESTTMP/local-amend-fold
  $ mkcommit ROOT
  $ mkcommit A0
  $ mkcommit B0
  $ hg amend -m "B1"
  $ hg log --hidden -G
  @  changeset:   3:b7ea6d14e664
  |  tag:         tip
  |  parent:      1:471f378eab4c
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     B1
  |
  | x  changeset:   2:0dec01379d3b
  |/   user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    obsolete:    reworded using amend as 3:b7ea6d14e664
  |    summary:     B0
  |
  o  changeset:   1:471f378eab4c
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     A0
  |
  o  changeset:   0:ea207398892e
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     ROOT
  
  $ hg fold --exact -r 'desc(A0) + desc(B1)' --date "0 0" -m "C0"
  2 changesets folded
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg log --hidden -G
  @  changeset:   4:eb5a0daa2192
  |  tag:         tip
  |  parent:      0:ea207398892e
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     C0
  |
  | x  changeset:   3:b7ea6d14e664
  | |  parent:      1:471f378eab4c
  | |  user:        test
  | |  date:        Thu Jan 01 00:00:00 1970 +0000
  | |  obsolete:    rewritten using fold as 4:eb5a0daa2192
  | |  summary:     B1
  | |
  | | x  changeset:   2:0dec01379d3b
  | |/   user:        test
  | |    date:        Thu Jan 01 00:00:00 1970 +0000
  | |    obsolete:    reworded using amend as 3:b7ea6d14e664
  | |    summary:     B0
  | |
  | x  changeset:   1:471f378eab4c
  |/   user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    obsolete:    rewritten using fold as 4:eb5a0daa2192
  |    summary:     A0
  |
  o  changeset:   0:ea207398892e
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     ROOT
  
 Actual test
 -----------

Check that debugobshistory on head show a coherent graph
  $ hg obslog eb5a0daa2192 --patch
  @    eb5a0daa2192 (4) C0
  |\
  x |  471f378eab4c (1) A0
   /     rewritten(description, content) as eb5a0daa2192 using fold by test (Thu Jan 01 00:00:00 1970 +0000)
  |        diff -r 471f378eab4c -r eb5a0daa2192 changeset-description
  |        --- a/changeset-description
  |        +++ b/changeset-description
  |        @@ -1,1 +1,1 @@
  |        -A0
  |        +C0
  |
  |        diff -r 471f378eab4c -r eb5a0daa2192 B0
  |        --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  |        +++ b/B0	Thu Jan 01 00:00:00 1970 +0000
  |        @@ -0,0 +1,1 @@
  |        +B0
  |
  |
  x  b7ea6d14e664 (3) B1
  |    rewritten(description, parent, content) as eb5a0daa2192 using fold by test (Thu Jan 01 00:00:00 1970 +0000)
  |      (No patch available, changesets rebased)
  |
  x  0dec01379d3b (2) B0
       rewritten(description) as b7ea6d14e664 using amend by test (Thu Jan 01 00:00:00 1970 +0000)
         diff -r 0dec01379d3b -r b7ea6d14e664 changeset-description
         --- a/changeset-description
         +++ b/changeset-description
         @@ -1,1 +1,1 @@
         -B0
         +B1
  
  
Check that obslog on ROOT with all option show everything
  $ hg obslog 1 --hidden --all --patch
  @    eb5a0daa2192 (4) C0
  |\
  x |  471f378eab4c (1) A0
   /     rewritten(description, content) as eb5a0daa2192 using fold by test (Thu Jan 01 00:00:00 1970 +0000)
  |        diff -r 471f378eab4c -r eb5a0daa2192 changeset-description
  |        --- a/changeset-description
  |        +++ b/changeset-description
  |        @@ -1,1 +1,1 @@
  |        -A0
  |        +C0
  |
  |        diff -r 471f378eab4c -r eb5a0daa2192 B0
  |        --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  |        +++ b/B0	Thu Jan 01 00:00:00 1970 +0000
  |        @@ -0,0 +1,1 @@
  |        +B0
  |
  |
  x  b7ea6d14e664 (3) B1
  |    rewritten(description, parent, content) as eb5a0daa2192 using fold by test (Thu Jan 01 00:00:00 1970 +0000)
  |      (No patch available, changesets rebased)
  |
  x  0dec01379d3b (2) B0
       rewritten(description) as b7ea6d14e664 using amend by test (Thu Jan 01 00:00:00 1970 +0000)
         diff -r 0dec01379d3b -r b7ea6d14e664 changeset-description
         --- a/changeset-description
         +++ b/changeset-description
         @@ -1,1 +1,1 @@
         -B0
         +B1
  
  
  $ hg obslog eb5a0daa2192 --no-graph -Tjson | python -m json.tool
  [
      {
          "markers": [],
          "node": "eb5a0daa2192",
          "rev": 4,
          "shortdescription": "C0"
      },
      {
          "markers": [
              {
                  "date": [
                      *, (glob)
                      0 (glob)
                  ],
                  "effect": [
                      *, (glob)
                      *, (glob)
                      "content"
                  ],
                  "operation": "fold",
                  "succnodes": [
                      "eb5a0daa2192"
                  ],
                  "user": "test",
                  "verb": "rewritten"
              }
          ],
          "node": "b7ea6d14e664",
          "rev": 3,
          "shortdescription": "B1"
      },
      {
          "markers": [
              {
                  "date": [
                      *, (glob)
                      0 (glob)
                  ],
                  "effect": [
                      "description"
                  ],
                  "operation": "amend",
                  "succnodes": [
                      "b7ea6d14e664"
                  ],
                  "user": "test",
                  "verb": "rewritten"
              }
          ],
          "node": "0dec01379d3b",
          "rev": 2,
          "shortdescription": "B0"
      },
      {
          "markers": [
              {
                  "date": [
                      *, (glob)
                      0 (glob)
                  ],
                  "effect": [
                      "description",
                      "content"
                  ],
                  "operation": "fold",
                  "succnodes": [
                      "eb5a0daa2192"
                  ],
                  "user": "test",
                  "verb": "rewritten"
              }
          ],
          "node": "471f378eab4c",
          "rev": 1,
          "shortdescription": "A0"
      }
  ]
  $ hg update 471f378eab4c
  abort: hidden revision '471f378eab4c' was rewritten as: eb5a0daa2192!
  (use --hidden to access hidden revisions)
  [255]
  $ hg update --hidden 'desc(A0)'
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  updated to hidden changeset 471f378eab4c
  (hidden revision '471f378eab4c' was rewritten as: eb5a0daa2192)
  working directory parent is obsolete! (471f378eab4c)
  (use 'hg evolve' to update to its successor: eb5a0daa2192)
  $ hg update --hidden 0dec01379d3b
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  updated to hidden changeset 0dec01379d3b
  (hidden revision '0dec01379d3b' was rewritten as: eb5a0daa2192)
  working directory parent is obsolete! (0dec01379d3b)
  (use 'hg evolve' to update to its successor: eb5a0daa2192)
  $ hg update 0dec01379d3b
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg update --hidden 'desc(B0)'
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
