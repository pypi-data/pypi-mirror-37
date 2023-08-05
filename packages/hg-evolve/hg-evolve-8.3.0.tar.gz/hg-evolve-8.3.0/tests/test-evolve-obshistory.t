This test file test the various messages when accessing obsolete
revisions.

Global setup
============

  $ . $TESTDIR/testlib/obshistory_setup.sh

Test simple common cases
========================

Test setup
----------
  $ hg init $TESTTMP/simple
  $ cd $TESTTMP/simple

Actual test
-----------
  $ hg obslog -ap null
  @  000000000000 (-1)
  
  $ hg obslog 'wdir()'
  abort: working directory revision cannot be specified
  [255]

Test output with pushed and pulled obs markers
==============================================

Test setup
----------

  $ hg init $TESTTMP/local-remote-markers-1
  $ cd $TESTTMP/local-remote-markers-1
  $ mkcommit ROOT
  $ mkcommit A0
  $ hg log --hidden -G
  @  changeset:   1:471f378eab4c
  |  tag:         tip
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     A0
  |
  o  changeset:   0:ea207398892e
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     ROOT
  
  $ hg clone $TESTTMP/local-remote-markers-1 $TESTTMP/local-remote-markers-2
  updating to branch default
  2 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ cd $TESTTMP/local-remote-markers-2
  $ hg log --hidden -G
  @  changeset:   1:471f378eab4c
  |  tag:         tip
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     A0
  |
  o  changeset:   0:ea207398892e
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     ROOT
  
  $ cd $TESTTMP/local-remote-markers-1
  $ hg amend -m "A1"
  $ hg amend -m "A2"
  $ hg log --hidden -G
  @  changeset:   3:7a230b46bf61
  |  tag:         tip
  |  parent:      0:ea207398892e
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     A2
  |
  | x  changeset:   2:fdf9bde5129a
  |/   parent:      0:ea207398892e
  |    user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    obsolete:    reworded using amend as 3:7a230b46bf61
  |    summary:     A1
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
  
 Actual test
 -----------

  $ hg obslog 7a230b46bf61 --patch
  @  7a230b46bf61 (3) A2
  |
  x  fdf9bde5129a (2) A1
  |    rewritten(description) as 7a230b46bf61 using amend by test (Thu Jan 01 00:00:00 1970 +0000)
  |      diff -r fdf9bde5129a -r 7a230b46bf61 changeset-description
  |      --- a/changeset-description
  |      +++ b/changeset-description
  |      @@ -1,1 +1,1 @@
  |      -A1
  |      +A2
  |
  |
  x  471f378eab4c (1) A0
       rewritten(description) as fdf9bde5129a using amend by test (Thu Jan 01 00:00:00 1970 +0000)
         diff -r 471f378eab4c -r fdf9bde5129a changeset-description
         --- a/changeset-description
         +++ b/changeset-description
         @@ -1,1 +1,1 @@
         -A0
         +A1
  
  
  $ cd $TESTTMP/local-remote-markers-2
  $ hg pull
  pulling from $TESTTMP/local-remote-markers-1
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 0 changes to 1 files (+1 heads)
  2 new obsolescence markers
  obsoleted 1 changesets
  new changesets 7a230b46bf61
  (run 'hg heads' to see heads, 'hg merge' to merge)
  working directory parent is obsolete! (471f378eab4c)
  (use 'hg evolve' to update to its successor: 7a230b46bf61)
Check that debugobshistory works with markers pointing to missing local
changectx
  $ hg obslog 7a230b46bf61 --patch
  o  7a230b46bf61 (2) A2
  |
  x  fdf9bde5129a
  |    rewritten(description) as 7a230b46bf61 using amend by test (Thu Jan 01 00:00:00 1970 +0000)
  |      (No patch available, context is not local)
  |
  @  471f378eab4c (1) A0
       rewritten(description) as fdf9bde5129a using amend by test (Thu Jan 01 00:00:00 1970 +0000)
         (No patch available, successor is unknown locally)
  

  $ hg obslog 7a230b46bf61 --patch -f
  o  7a230b46bf61 (2) A2
  |
  @  471f378eab4c (1) A0
       reworded(description) as 7a230b46bf61 using amend by test (at Thu Jan 01 00:00:00 1970 +0000)
         diff -r 471f378eab4c -r 7a230b46bf61 changeset-description
         --- a/changeset-description
         +++ b/changeset-description
         @@ -1,1 +1,1 @@
         -A0
         +A2
  
  
  $ hg obslog 7a230b46bf61 --color=debug --patch
  o  [evolve.node|7a230b46bf61] [evolve.rev|(2)] [evolve.short_description|A2]
  |
  x  [evolve.node evolve.missing_change_ctx|fdf9bde5129a]
  |    [evolve.verb|rewritten](description) as [evolve.node|7a230b46bf61] using [evolve.operation|amend] by [evolve.user|test] [evolve.date|(Thu Jan 01 00:00:00 1970 +0000)]
  |      (No patch available, context is not local)
  |
  @  [evolve.node|471f378eab4c] [evolve.rev|(1)] [evolve.short_description|A0]
       [evolve.verb|rewritten](description) as [evolve.node|fdf9bde5129a] using [evolve.operation|amend] by [evolve.user|test] [evolve.date|(Thu Jan 01 00:00:00 1970 +0000)]
         (No patch available, successor is unknown locally)
  
