Tests for the --stop flag for `hg evolve` command while resolving phase-divergence
==================================================================================

The `--stop` flag stops the interrupted evolution and delete the state file so
user can do other things and comeback and do evolution later on

This is testing cases when `hg evolve` command is doing phase-divergence resolution.

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

Creating phase divergence, resolution of which will lead to conflicts
----------------------------------------------------------------------

  $ hg up .^^^
  0 files updated, 0 files merged, 3 files removed, 0 files unresolved
  $ hg pick -r .~-3
  picking 4:c41c793e0ef1 "added d"
  $ echo foobar > c
  $ hg add c
  $ hg amend

  $ hg glog --hidden
  @  6:ddba58020bc0 added d
  |   () draft
  | x  5:cfe30edc6125 added d
  |/    () draft
  | x  4:c41c793e0ef1 added d
  | |   () draft
  | o  3:ca1b80f7960a added c
  | |   () draft
  | o  2:b1661037fa25 added b
  |/    () draft
  o  1:c7586e2a9264 added a
  |   () draft
  o  0:8fa14d15e168 added hgignore
      () draft

  $ hg phase -r c41c793e0ef1 --public --hidden
  1 new phase-divergent changesets

  $ hg glog
  @  6:ddba58020bc0 added d
  |   () draft
  | o  4:c41c793e0ef1 added d
  | |   () public
  | o  3:ca1b80f7960a added c
  | |   () public
  | o  2:b1661037fa25 added b
  |/    () public
  o  1:c7586e2a9264 added a
  |   () public
  o  0:8fa14d15e168 added hgignore
      () public
  $ hg evolve --phase-divergent
  recreate:[6] added d
  atop:[4] added d
  rebasing to destination parent: ca1b80f7960a
  merging c
  warning: conflicts while merging c! (edit, then use 'hg resolve --mark')
  fix conflicts and see `hg help evolve.interrupted`
  [1]

  $ hg evolve --stop
  stopped the interrupted evolve
  working directory is now at ca1b80f7960a

XXX: maybe we should update wdir to where it was
  $ hg glog
  *  6:ddba58020bc0 added d
  |   () draft
  | o  4:c41c793e0ef1 added d
  | |   () public
  | @  3:ca1b80f7960a added c
  | |   () public
  | o  2:b1661037fa25 added b
  |/    () public
  o  1:c7586e2a9264 added a
  |   () public
  o  0:8fa14d15e168 added hgignore
      () public
