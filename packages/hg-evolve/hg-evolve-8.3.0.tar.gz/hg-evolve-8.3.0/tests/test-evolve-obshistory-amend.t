This test file test the various messages when accessing obsolete
revisions.

Global setup
============

  $ . $TESTDIR/testlib/obshistory_setup.sh


Test output on amended commit
=============================

Test setup
----------

  $ hg init $TESTTMP/local-amend
  $ hg init $TESTTMP/server
  $ cd $TESTTMP/local-amend
  $ mkcommit ROOT
  $ sync
  $ mkcommit A0 .
  $ echo 42 >> A0
  $ hg amend -m "A1
  > 
  > Better commit message"
  $ sync
  $ hg log --hidden -G
  @  changeset:   2:4ae3a4151de9
  |  tag:         tip
  |  parent:      0:ea207398892e
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     A1
  |
  | x  changeset:   1:471f378eab4c
  |/   user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    obsolete:    rewritten using amend as 2:4ae3a4151de9
  |    summary:     A0
  |
  o  changeset:   0:ea207398892e
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     ROOT
  
Check output on the client side
-------------------------------
  $ hg obslog --patch 4ae3a4151de9
  @  4ae3a4151de9 (2) A1
  |
  x  471f378eab4c (1) A0
       rewritten(description, content) as 4ae3a4151de9 using amend by test (*) (glob)
         diff -r 471f378eab4c -r 4ae3a4151de9 changeset-description
         --- a/changeset-description
         +++ b/changeset-description
         @@ -1,1 +1,3 @@
         -A0
         +A1
         +
         +Better commit message
  
         diff -r 471f378eab4c -r 4ae3a4151de9 A0
         --- a/A0	Thu Jan 01 00:00:00 1970 +0000
         +++ b/A0	Thu Jan 01 00:00:00 1970 +0000
         @@ -1,1 +1,2 @@
          A0
         +42
  
  
  $ hg obslog --patch --color debug
  @  [evolve.node|4ae3a4151de9] [evolve.rev|(2)] [evolve.short_description|A1]
  |
  x  [evolve.node|471f378eab4c] [evolve.rev|(1)] [evolve.short_description|A0]
       [evolve.verb|rewritten](description, content) as [evolve.node|4ae3a4151de9] using [evolve.operation|amend] by [evolve.user|test] [evolve.date|(Thu Jan 01 00:00:00 1970 +0000)]
         [diff.diffline|diff -r 471f378eab4c -r 4ae3a4151de9 changeset-description]
         [diff.file_a|--- a/changeset-description]
         [diff.file_b|+++ b/changeset-description]
         [diff.hunk|@@ -1,1 +1,3 @@]
         [diff.deleted|-A0]
         [diff.inserted|+A1]
         [diff.inserted|+]
         [diff.inserted|+Better commit message]
  
         [diff.diffline|diff -r 471f378eab4c -r 4ae3a4151de9 A0]
         [diff.file_a|--- a/A0	Thu Jan 01 00:00:00 1970 +0000]
         [diff.file_b|+++ b/A0	Thu Jan 01 00:00:00 1970 +0000]
         [diff.hunk|@@ -1,1 +1,2 @@]
          A0
         [diff.inserted|+42]
  
  

  $ hg obslog --no-graph --patch 4ae3a4151de9
  4ae3a4151de9 (2) A1
  471f378eab4c (1) A0
    rewritten(description, content) as 4ae3a4151de9 using amend by test (Thu Jan 01 00:00:00 1970 +0000)
      diff -r 471f378eab4c -r 4ae3a4151de9 changeset-description
      --- a/changeset-description
      +++ b/changeset-description
      @@ -1,1 +1,3 @@
      -A0
      +A1
      +
      +Better commit message
  
      diff -r 471f378eab4c -r 4ae3a4151de9 A0
      --- a/A0	Thu Jan 01 00:00:00 1970 +0000
      +++ b/A0	Thu Jan 01 00:00:00 1970 +0000
      @@ -1,1 +1,2 @@
       A0
      +42
  

  $ hg obslog 4ae3a4151de9 --graph -T'{label("log.summary", shortdescription)} {if(markers, join(markers % "at {date|hgdate} by {user|person} ", " also "))}'
  @  A1
  |
  x  A0 at 0 0 by test
  
  $ hg obslog 4ae3a4151de9 --no-graph -Tjson | python -m json.tool
  [
      {
          "markers": [],
          "node": "4ae3a4151de9",
          "rev": 2,
          "shortdescription": "A1"
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
                  "operation": "amend",
                  "succnodes": [
                      "4ae3a4151de9"
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
  $ hg obslog --hidden --patch 471f378eab4c
  x  471f378eab4c (1) A0
       rewritten(description, content) as 4ae3a4151de9 using amend by test (Thu Jan 01 00:00:00 1970 +0000)
         diff -r 471f378eab4c -r 4ae3a4151de9 changeset-description
         --- a/changeset-description
         +++ b/changeset-description
         @@ -1,1 +1,3 @@
         -A0
         +A1
         +
         +Better commit message
  
         diff -r 471f378eab4c -r 4ae3a4151de9 A0
         --- a/A0	Thu Jan 01 00:00:00 1970 +0000
         +++ b/A0	Thu Jan 01 00:00:00 1970 +0000
         @@ -1,1 +1,2 @@
          A0
         +42
  
  
  $ hg obslog --hidden 471f378eab4c --no-graph -Tjson | python -m json.tool
  [
      {
          "markers": [
              {
                  "date": [
                      *, (glob)
                      0 (glob)
                  ],
                  "effect": [
                      *, (glob)
                      "content"
                  ],
                  "operation": "amend",
                  "succnodes": [
                      "4ae3a4151de9"
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
  abort: hidden revision '471f378eab4c' was rewritten as: 4ae3a4151de9!
  (use --hidden to access hidden revisions)
  [255]
  $ hg update --hidden "desc(A0)"
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  updated to hidden changeset 471f378eab4c
  (hidden revision '471f378eab4c' was rewritten as: 4ae3a4151de9)
  working directory parent is obsolete! (471f378eab4c)
  (use 'hg evolve' to update to its successor: 4ae3a4151de9)

Check output on the server side
-------------------------------

  $ hg obslog -R $TESTTMP/server --patch 4ae3a4151de9
  o  4ae3a4151de9 (1) A1
  |
  x  471f378eab4c
       rewritten(description, content) as 4ae3a4151de9 using amend by test (Thu Jan 01 00:00:00 1970 +0000)
         (No patch available, context is not local)
  
  $ hg obslog -R $TESTTMP/server -f --patch 4ae3a4151de9
  o  4ae3a4151de9 (1) A1
  
  $ hg obslog -R $TESTTMP/server --no-graph --patch 4ae3a4151de9
  4ae3a4151de9 (1) A1
  471f378eab4c
    rewritten(description, content) as 4ae3a4151de9 using amend by test (Thu Jan 01 00:00:00 1970 +0000)
      (No patch available, context is not local)

  $ hg obslog -R $TESTTMP/server --no-graph -f --patch 4ae3a4151de9
  4ae3a4151de9 (1) A1
  471f378eab4c
    rewritten(description, content) as 4ae3a4151de9 using amend by test (Thu Jan 01 00:00:00 1970 +0000)
      (No patch available, context is not local)

Amend two more times
====================

Amend again
-----------
  $ hg log --hidden -G
  o  changeset:   2:4ae3a4151de9
  |  tag:         tip
  |  parent:      0:ea207398892e
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     A1
  |
  | @  changeset:   1:471f378eab4c
  |/   user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    obsolete:    rewritten using amend as 2:4ae3a4151de9
  |    summary:     A0
  |
  o  changeset:   0:ea207398892e
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     ROOT
  
  $ hg up tip
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg amend -m "A2
  > 
  > Better better commit message"
  $ hg amend -m "A3
  > 
  > Better better better commit message"
  $ sync
  $ hg log --hidden -G
  @  changeset:   4:92210308515b
  |  tag:         tip
  |  parent:      0:ea207398892e
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     A3
  |
  | x  changeset:   3:4f1685185907
  |/   parent:      0:ea207398892e
  |    user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    obsolete:    reworded using amend as 4:92210308515b
  |    summary:     A2
  |
  | x  changeset:   2:4ae3a4151de9
  |/   parent:      0:ea207398892e
  |    user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    obsolete:    reworded using amend as 3:4f1685185907
  |    summary:     A1
  |
  | x  changeset:   1:471f378eab4c
  |/   user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    obsolete:    rewritten using amend as 2:4ae3a4151de9
  |    summary:     A0
  |
  o  changeset:   0:ea207398892e
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     ROOT
  
Check the output on the client
------------------------------

  $ hg obslog --patch 92210308515b
  @  92210308515b (4) A3
  |
  x  4f1685185907 (3) A2
  |    rewritten(description) as 92210308515b using amend by test (Thu Jan 01 00:00:00 1970 +0000)
  |      diff -r 4f1685185907 -r 92210308515b changeset-description
  |      --- a/changeset-description
  |      +++ b/changeset-description
  |      @@ -1,3 +1,3 @@
  |      -A2
  |      +A3
  |
  |      -Better better commit message
  |      +Better better better commit message
  |
  |
  x  4ae3a4151de9 (2) A1
  |    rewritten(description) as 4f1685185907 using amend by test (Thu Jan 01 00:00:00 1970 +0000)
  |      diff -r 4ae3a4151de9 -r 4f1685185907 changeset-description
  |      --- a/changeset-description
  |      +++ b/changeset-description
  |      @@ -1,3 +1,3 @@
  |      -A1
  |      +A2
  |
  |      -Better commit message
  |      +Better better commit message
  |
  |
  x  471f378eab4c (1) A0
       rewritten(description, content) as 4ae3a4151de9 using amend by test (Thu Jan 01 00:00:00 1970 +0000)
         diff -r 471f378eab4c -r 4ae3a4151de9 changeset-description
         --- a/changeset-description
         +++ b/changeset-description
         @@ -1,1 +1,3 @@
         -A0
         +A1
         +
         +Better commit message
  
         diff -r 471f378eab4c -r 4ae3a4151de9 A0
         --- a/A0	Thu Jan 01 00:00:00 1970 +0000
         +++ b/A0	Thu Jan 01 00:00:00 1970 +0000
         @@ -1,1 +1,2 @@
          A0
         +42
  
  
Check the output on the server
------------------------------

  $ hg obslog -R $TESTTMP/server --patch 92210308515b
  o  92210308515b (2) A3
  |
  x  4f1685185907
  |    rewritten(description) as 92210308515b using amend by test (Thu Jan 01 00:00:00 1970 +0000)
  |      (No patch available, context is not local)
  |
  x  4ae3a4151de9 (1) A1
  |    rewritten(description) as 4f1685185907 using amend by test (Thu Jan 01 00:00:00 1970 +0000)
  |      (No patch available, successor is unknown locally)
  |
  x  471f378eab4c
       rewritten(description, content) as 4ae3a4151de9 using amend by test (Thu Jan 01 00:00:00 1970 +0000)
         (No patch available, context is not local)
  
  $ hg obslog -R $TESTTMP/server -f --patch 92210308515b
  o  92210308515b (2) A3
  |
  x  4ae3a4151de9 (1) A1
       reworded(description) as 92210308515b using amend by test (at Thu Jan 01 00:00:00 1970 +0000)
         diff -r 4ae3a4151de9 -r 92210308515b changeset-description
         --- a/changeset-description
         +++ b/changeset-description
         @@ -1,3 +1,3 @@
         -A1
         +A3
  
         -Better commit message
         +Better better better commit message
  
  
  $ hg obslog -R $TESTTMP/server --no-graph --patch 92210308515b
  92210308515b (2) A3
  4f1685185907
    rewritten(description) as 92210308515b using amend by test (Thu Jan 01 00:00:00 1970 +0000)
      (No patch available, context is not local)
  4ae3a4151de9 (1) A1
    rewritten(description) as 4f1685185907 using amend by test (Thu Jan 01 00:00:00 1970 +0000)
      (No patch available, successor is unknown locally)
  471f378eab4c
    rewritten(description, content) as 4ae3a4151de9 using amend by test (Thu Jan 01 00:00:00 1970 +0000)
      (No patch available, context is not local)

  $ hg obslog -R $TESTTMP/server --no-graph -f --patch 92210308515b
  92210308515b (2) A3
  4f1685185907
    rewritten(description) as 92210308515b using amend by test (Thu Jan 01 00:00:00 1970 +0000)
      (No patch available, context is not local)
  4ae3a4151de9 (1) A1
    rewritten(description) as 4f1685185907 using amend by test (Thu Jan 01 00:00:00 1970 +0000)
      (No patch available, successor is unknown locally)
  471f378eab4c
    rewritten(description, content) as 4ae3a4151de9 using amend by test (Thu Jan 01 00:00:00 1970 +0000)
      (No patch available, context is not local)
