Testing the `--no-update` flag to `hg evolve` command
=====================================================

There is an `--update` flag to `hg evolve` command which defaults to True. The
`--update` flag updates to the head of the evolved revisions. If you dont want
to change your working directory or update your working directory to its
sucessor after hg evolve, `hg evolve --no-update` is the thing for you.

This patch tests that flag.

Setup
-----

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

Making sure we stay where we were is current wdir parent is not obsoleted
--------------------------------------------------------------------------

  $ hg up .^^
  0 files updated, 0 files merged, 2 files removed, 0 files unresolved
  $ echo bar > b
  $ hg amend
  2 new orphan changesets
  $ hg glog
  @  5:7ed0642d644b added b
  |   () draft
  | *  4:c41c793e0ef1 added d
  | |   () draft
  | *  3:ca1b80f7960a added c
  | |   () draft
  | x  2:b1661037fa25 added b
  |/    () draft
  o  1:c7586e2a9264 added a
  |   () draft
  o  0:8fa14d15e168 added hgignore
      () draft

There is 'working directory is now at' message because it didnt changed
  $ hg evolve --all --no-update
  move:[3] added c
  atop:[5] added b
  move:[4] added d

  $ hg glog
  o  7:b6b20b8eefdc added d
  |   () draft
  o  6:7c46f743e62f added c
  |   () draft
  @  5:7ed0642d644b added b
  |   () draft
  o  1:c7586e2a9264 added a
  |   () draft
  o  0:8fa14d15e168 added hgignore
      () draft

Updating to successor when working directory parent is obsoleted by evolution
-----------------------------------------------------------------------------

  $ hg prev
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  [1] added a
  $ echo bar > a
  $ hg amend
  3 new orphan changesets
  $ hg up 7ed0642d644b
  2 files updated, 0 files merged, 0 files removed, 0 files unresolved

  $ hg glog
  o  8:3d41537b44ca added a
  |   () draft
  | *  7:b6b20b8eefdc added d
  | |   () draft
  | *  6:7c46f743e62f added c
  | |   () draft
  | @  5:7ed0642d644b added b
  | |   () draft
  | x  1:c7586e2a9264 added a
  |/    () draft
  o  0:8fa14d15e168 added hgignore
      () draft

  $ hg evolve --all --any --no-update
  move:[5] added b
  atop:[8] added a
  move:[6] added c
  move:[7] added d
  working directory is now at 12c720cb3782

  $ hg glog
  o  11:a74d9f22ba3f added d
  |   () draft
  o  10:958f5155e8cd added c
  |   () draft
  @  9:12c720cb3782 added b
  |   () draft
  o  8:3d41537b44ca added a
  |   () draft
  o  0:8fa14d15e168 added hgignore
      () draft
