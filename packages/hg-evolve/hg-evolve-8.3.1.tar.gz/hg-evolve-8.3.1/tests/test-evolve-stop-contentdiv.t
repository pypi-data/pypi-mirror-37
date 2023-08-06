Tests for the --stop flag for `hg evolve` command while resolving content-divergence
==================================================================================

The `--stop` flag stops the interrupted evolution and delete the state file so
user can do other things and comeback and do evolution later on

This is testing cases when `hg evolve` command is doing content-divergence resolution.

Setup
=====

  $ cat >> $HGRCPATH <<EOF
  > [alias]
  > glog = log -GT "{rev}:{node|short} {desc}\n ({bookmarks}) {phase}"
  > [extensions]
  > EOF
  $ echo "evolve=$(echo $(dirname $TESTDIR))/hgext3rd/evolve/" >> $HGRCPATH

  $ hg init stoprepo
  $ cd stoprepo
  $ echo ".*\.orig" > .hgignore
  $ hg add .hgignore
  $ hg ci -m "added hgignore"
  $ for ch in a b c d; do echo foo > $ch; hg add $ch; hg ci -qm "added "$ch; done;

  $ hg glog
  @  4:c41c793e0ef1 added d
  |   () draft
  o  3:ca1b80f7960a added c
  |   () draft
  o  2:b1661037fa25 added b
  |   () draft
  o  1:c7586e2a9264 added a
  |   () draft
  o  0:8fa14d15e168 added hgignore
      () draft

Creating content divergence, resolution of which will lead to conflicts
-----------------------------------------------------------------------

  $ echo bar > d
  $ hg amend

  $ hg up c41c793e0ef1 --hidden
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  updated to hidden changeset c41c793e0ef1
  (hidden revision 'c41c793e0ef1' was rewritten as: e49523854bc8)
  working directory parent is obsolete! (c41c793e0ef1)
  (use 'hg evolve' to update to its successor: e49523854bc8)

  $ echo foobar > d
  $ hg amend
  2 new content-divergent changesets
  $ hg glog --hidden
  @  6:9c1631e352d9 added d
  |   () draft
  | *  5:e49523854bc8 added d
  |/    () draft
  | x  4:c41c793e0ef1 added d
  |/    () draft
  o  3:ca1b80f7960a added c
  |   () draft
  o  2:b1661037fa25 added b
  |   () draft
  o  1:c7586e2a9264 added a
  |   () draft
  o  0:8fa14d15e168 added hgignore
      () draft

  $ hg evolve --content-divergent
  merge:[6] added d
  with: [5] added d
  base: [4] added d
  merging "other" content-divergent changeset 'e49523854bc8'
  merging d
  warning: conflicts while merging d! (edit, then use 'hg resolve --mark')
  0 files updated, 0 files merged, 0 files removed, 1 files unresolved
  fix conflicts and see `hg help evolve.interrupted`
  [1]

  $ hg evolve --stop
  stopped the interrupted evolve
  working directory is now at 9c1631e352d9

  $ hg glog --hidden
  @  6:9c1631e352d9 added d
  |   () draft
  | *  5:e49523854bc8 added d
  |/    () draft
  | x  4:c41c793e0ef1 added d
  |/    () draft
  o  3:ca1b80f7960a added c
  |   () draft
  o  2:b1661037fa25 added b
  |   () draft
  o  1:c7586e2a9264 added a
  |   () draft
  o  0:8fa14d15e168 added hgignore
      () draft

Content divergence with parent change which will result in conflicts while
merging
---------------------------------------------------------------------------

  $ hg rebase -r . -d .^^^ --config extensions.rebase=
  rebasing 6:9c1631e352d9 "added d" (tip)

  $ hg glog
  @  7:517d4375cb72 added d
  |   () draft
  | *  5:e49523854bc8 added d
  | |   () draft
  | o  3:ca1b80f7960a added c
  | |   () draft
  | o  2:b1661037fa25 added b
  |/    () draft
  o  1:c7586e2a9264 added a
  |   () draft
  o  0:8fa14d15e168 added hgignore
      () draft

  $ hg evolve --content-divergent
  merge:[5] added d
  with: [7] added d
  base: [4] added d
  rebasing "other" content-divergent changeset 517d4375cb72 on ca1b80f7960a
  updating to "local" side of the conflict: e49523854bc8
  merging "other" content-divergent changeset '606ad96040fc'
  merging d
  warning: conflicts while merging d! (edit, then use 'hg resolve --mark')
  0 files updated, 0 files merged, 0 files removed, 1 files unresolved
  fix conflicts and see `hg help evolve.interrupted`
  [1]

  $ hg evolve --stop
  stopped the interrupted evolve
  working directory is now at 517d4375cb72

  $ hg glog
  @  7:517d4375cb72 added d
  |   () draft
  | *  5:e49523854bc8 added d
  | |   () draft
  | o  3:ca1b80f7960a added c
  | |   () draft
  | o  2:b1661037fa25 added b
  |/    () draft
  o  1:c7586e2a9264 added a
  |   () draft
  o  0:8fa14d15e168 added hgignore
      () draft

Content-divergence with parent-change which will result in conflicts while
relocation
---------------------------------------------------------------------------

  $ echo babar > c
  $ hg add c
  $ hg amend
  $ hg glog
  @  8:8fd1c4bd144c added d
  |   () draft
  | *  5:e49523854bc8 added d
  | |   () draft
  | o  3:ca1b80f7960a added c
  | |   () draft
  | o  2:b1661037fa25 added b
  |/    () draft
  o  1:c7586e2a9264 added a
  |   () draft
  o  0:8fa14d15e168 added hgignore
      () draft

  $ hg evolve --content-divergent
  merge:[5] added d
  with: [8] added d
  base: [4] added d
  rebasing "other" content-divergent changeset 8fd1c4bd144c on ca1b80f7960a
  merging c
  warning: conflicts while merging c! (edit, then use 'hg resolve --mark')
  fix conflicts and see `hg help evolve.interrupted`
  [1]

  $ hg diff
  diff -r ca1b80f7960a c
  --- a/c	Thu Jan 01 00:00:00 1970 +0000
  +++ b/c	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,1 +1,5 @@
  +<<<<<<< destination: ca1b80f7960a - test: added c
   foo
  +=======
  +babar
  +>>>>>>> evolving:    8fd1c4bd144c - test: added d
  diff -r ca1b80f7960a d
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/d	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +foobar

  $ hg evolve --stop
  stopped the interrupted evolve
  working directory is now at ca1b80f7960a

XXX: we should have preserved the wdir to be at rev 8
  $ hg glog
  *  8:8fd1c4bd144c added d
  |   () draft
  | *  5:e49523854bc8 added d
  | |   () draft
  | @  3:ca1b80f7960a added c
  | |   () draft
  | o  2:b1661037fa25 added b
  |/    () draft
  o  1:c7586e2a9264 added a
  |   () draft
  o  0:8fa14d15e168 added hgignore
      () draft
