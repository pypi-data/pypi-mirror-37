This test file test the various messages when accessing obsolete
revisions.

Global setup
============

  $ . $TESTDIR/testlib/obshistory_setup.sh

Test output with content-divergence
===================================

Test setup
----------

  $ hg init $TESTTMP/local-divergence
  $ cd $TESTTMP/local-divergence
  $ mkcommit ROOT
  $ mkcommit A0
  $ hg amend -m "A1"
  $ hg log --hidden -G
  @  changeset:   2:fdf9bde5129a
  |  tag:         tip
  |  parent:      0:ea207398892e
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     A1
  |
  | x  changeset:   1:471f378eab4c
  |/   user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    obsolete:    reworded using amend as 2:fdf9bde5129a
  |    summary:     A0
  |
  o  changeset:   0:ea207398892e
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     ROOT
  
  $ hg update --hidden 'desc(A0)'
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  updated to hidden changeset 471f378eab4c
  (hidden revision '471f378eab4c' was rewritten as: fdf9bde5129a)
  working directory parent is obsolete! (471f378eab4c)
  (use 'hg evolve' to update to its successor: fdf9bde5129a)
  $ hg amend -m "A2"
  2 new content-divergent changesets
  $ hg log --hidden -G
  @  changeset:   3:65b757b745b9
  |  tag:         tip
  |  parent:      0:ea207398892e
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  instability: content-divergent
  |  summary:     A2
  |
  | *  changeset:   2:fdf9bde5129a
  |/   parent:      0:ea207398892e
  |    user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    instability: content-divergent
  |    summary:     A1
  |
  | x  changeset:   1:471f378eab4c
  |/   user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    obsolete:    reworded using amend as 2:fdf9bde5129a
  |    obsolete:    reworded using amend as 3:65b757b745b9
  |    summary:     A0
  |
  o  changeset:   0:ea207398892e
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     ROOT
  
Actual test
-----------

Check that debugobshistory on the divergent revision show both destinations
  $ hg obslog --hidden 471f378eab4c --patch
  x  471f378eab4c (1) A0
       rewritten(description) as 65b757b745b9 using amend by test (Thu Jan 01 00:00:00 1970 +0000)
         diff -r 471f378eab4c -r 65b757b745b9 changeset-description
         --- a/changeset-description
         +++ b/changeset-description
         @@ -1,1 +1,1 @@
         -A0
         +A2
  
       rewritten(description) as fdf9bde5129a using amend by test (Thu Jan 01 00:00:00 1970 +0000)
         diff -r 471f378eab4c -r fdf9bde5129a changeset-description
         --- a/changeset-description
         +++ b/changeset-description
         @@ -1,1 +1,1 @@
         -A0
         +A1
  
  

Check that with all option, every changeset is shown
  $ hg obslog --hidden --all 471f378eab4c --patch
  @  65b757b745b9 (3) A2
  |
  | *  fdf9bde5129a (2) A1
  |/
  x  471f378eab4c (1) A0
       rewritten(description) as 65b757b745b9 using amend by test (Thu Jan 01 00:00:00 1970 +0000)
         diff -r 471f378eab4c -r 65b757b745b9 changeset-description
         --- a/changeset-description
         +++ b/changeset-description
         @@ -1,1 +1,1 @@
         -A0
         +A2
  
       rewritten(description) as fdf9bde5129a using amend by test (Thu Jan 01 00:00:00 1970 +0000)
         diff -r 471f378eab4c -r fdf9bde5129a changeset-description
         --- a/changeset-description
         +++ b/changeset-description
         @@ -1,1 +1,1 @@
         -A0
         +A1
  
  
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
                      "description"
                  ],
                  "operation": "amend",
                  "succnodes": [
                      "65b757b745b9"
                  ],
                  "user": "test",
                  "verb": "rewritten"
              },
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
                      "fdf9bde5129a"
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
Check that debugobshistory on the first diverged revision show the revision
and the diverent one
  $ hg obslog fdf9bde5129a --patch
  *  fdf9bde5129a (2) A1
  |
  x  471f378eab4c (1) A0
       rewritten(description) as 65b757b745b9 using amend by test (Thu Jan 01 00:00:00 1970 +0000)
         diff -r 471f378eab4c -r 65b757b745b9 changeset-description
         --- a/changeset-description
         +++ b/changeset-description
         @@ -1,1 +1,1 @@
         -A0
         +A2
  
       rewritten(description) as fdf9bde5129a using amend by test (Thu Jan 01 00:00:00 1970 +0000)
         diff -r 471f378eab4c -r fdf9bde5129a changeset-description
         --- a/changeset-description
         +++ b/changeset-description
         @@ -1,1 +1,1 @@
         -A0
         +A1
  
  

Check that all option show all of them
  $ hg obslog fdf9bde5129a -a --patch
  @  65b757b745b9 (3) A2
  |
  | *  fdf9bde5129a (2) A1
  |/
  x  471f378eab4c (1) A0
       rewritten(description) as 65b757b745b9 using amend by test (Thu Jan 01 00:00:00 1970 +0000)
         diff -r 471f378eab4c -r 65b757b745b9 changeset-description
         --- a/changeset-description
         +++ b/changeset-description
         @@ -1,1 +1,1 @@
         -A0
         +A2
  
       rewritten(description) as fdf9bde5129a using amend by test (Thu Jan 01 00:00:00 1970 +0000)
         diff -r 471f378eab4c -r fdf9bde5129a changeset-description
         --- a/changeset-description
         +++ b/changeset-description
         @@ -1,1 +1,1 @@
         -A0
         +A1
  
  
Check that debugobshistory on the second diverged revision show the revision
and the diverent one
  $ hg obslog 65b757b745b9 --patch
  @  65b757b745b9 (3) A2
  |
  x  471f378eab4c (1) A0
       rewritten(description) as 65b757b745b9 using amend by test (Thu Jan 01 00:00:00 1970 +0000)
         diff -r 471f378eab4c -r 65b757b745b9 changeset-description
         --- a/changeset-description
         +++ b/changeset-description
         @@ -1,1 +1,1 @@
         -A0
         +A2
  
       rewritten(description) as fdf9bde5129a using amend by test (Thu Jan 01 00:00:00 1970 +0000)
         diff -r 471f378eab4c -r fdf9bde5129a changeset-description
         --- a/changeset-description
         +++ b/changeset-description
         @@ -1,1 +1,1 @@
         -A0
         +A1
  
  
Check that all option show all of them
  $ hg obslog 65b757b745b9 -a --patch
  @  65b757b745b9 (3) A2
  |
  | *  fdf9bde5129a (2) A1
  |/
  x  471f378eab4c (1) A0
       rewritten(description) as 65b757b745b9 using amend by test (Thu Jan 01 00:00:00 1970 +0000)
         diff -r 471f378eab4c -r 65b757b745b9 changeset-description
         --- a/changeset-description
         +++ b/changeset-description
         @@ -1,1 +1,1 @@
         -A0
         +A2
  
       rewritten(description) as fdf9bde5129a using amend by test (Thu Jan 01 00:00:00 1970 +0000)
         diff -r 471f378eab4c -r fdf9bde5129a changeset-description
         --- a/changeset-description
         +++ b/changeset-description
         @@ -1,1 +1,1 @@
         -A0
         +A1
  
  
Check that debugobshistory on the both diverged revision show a coherent
graph
  $ hg obslog '65b757b745b9+fdf9bde5129a' --patch
  @  65b757b745b9 (3) A2
  |
  | *  fdf9bde5129a (2) A1
  |/
  x  471f378eab4c (1) A0
       rewritten(description) as 65b757b745b9 using amend by test (Thu Jan 01 00:00:00 1970 +0000)
         diff -r 471f378eab4c -r 65b757b745b9 changeset-description
         --- a/changeset-description
         +++ b/changeset-description
         @@ -1,1 +1,1 @@
         -A0
         +A2
  
       rewritten(description) as fdf9bde5129a using amend by test (Thu Jan 01 00:00:00 1970 +0000)
         diff -r 471f378eab4c -r fdf9bde5129a changeset-description
         --- a/changeset-description
         +++ b/changeset-description
         @@ -1,1 +1,1 @@
         -A0
         +A1
  
  
  $ hg obslog '65b757b745b9+fdf9bde5129a' --no-graph -Tjson | python -m json.tool
  [
      {
          "markers": [],
          "node": "65b757b745b9",
          "rev": 3,
          "shortdescription": "A2"
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
                      "65b757b745b9"
                  ],
                  "user": "test",
                  "verb": "rewritten"
              },
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
                      "fdf9bde5129a"
                  ],
                  "user": "test",
                  "verb": "rewritten"
              }
          ],
          "node": "471f378eab4c",
          "rev": 1,
          "shortdescription": "A0"
      },
      {
          "markers": [],
          "node": "fdf9bde5129a",
          "rev": 2,
          "shortdescription": "A1"
      }
  ]
  $ hg update 471f378eab4c
  abort: hidden revision '471f378eab4c' has diverged!
  (use --hidden to access hidden revisions)
  [255]
  $ hg update --hidden 'desc(A0)'
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  updated to hidden changeset 471f378eab4c
  (hidden revision '471f378eab4c' has diverged)
  working directory parent is obsolete! (471f378eab4c)
  (471f378eab4c has diverged, use 'hg evolve --list --content-divergent' to resolve the issue)
