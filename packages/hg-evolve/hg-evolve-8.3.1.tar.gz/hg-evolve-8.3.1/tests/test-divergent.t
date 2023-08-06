Tests the resolution of divergence

  $ cat >> $HGRCPATH <<EOF
  > [defaults]
  > amend=-d "0 0"
  > fold=-d "0 0"
  > [web]
  > push_ssl = false
  > allow_push = *
  > [phases]
  > publish = False
  > [diff]
  > git = 1
  > unified = 0
  > [ui]
  > logtemplate = {rev}:{node|short}@{branch}({phase}) {desc|firstline} [{troubles}]\n
  > [extensions]
  > EOF
  $ echo "evolve=$(echo $(dirname $TESTDIR))/hgext3rd/evolve/" >> $HGRCPATH
  $ mkcommit() {
  >    echo "$1" > "$1"
  >    hg add "$1"
  >    hg ci -m "add $1"
  > }

  $ mkcommits() {
  >   for i in $@; do mkcommit $i ; done
  > }

Basic test of divergence: two divergent changesets with the same parents
With --all --any we dedupe the divergent and solve the divergence once

  $ hg init test1
  $ cd test1
  $ echo a > a
  $ hg ci -Aqm "added a"
  $ echo b > b
  $ hg ci -Aqm "added b"

  $ hg up .^
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ echo bdivergent > bdivergent1
  $ hg ci -Am "divergent"
  adding bdivergent1
  created new head

  $ hg up .^
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ echo bdivergent > bdivergent2
  $ hg ci -Am "divergent"
  adding bdivergent2
  created new head

  $ hg prune -s 8374d2ddc3a4 "desc('added b')"
  1 changesets pruned
  $ hg prune -s 593c57f2117e "desc('added b')" --hidden
  1 changesets pruned
  2 new content-divergent changesets

  $ hg log -G
  @  3:8374d2ddc3a4@default(draft) divergent [content-divergent]
  |
  | *  2:593c57f2117e@default(draft) divergent [content-divergent]
  |/
  o  0:9092f1db7931@default(draft) added a []
  

  $ hg evolve --all --any --content-divergent
  merge:[2] divergent
  with: [3] divergent
  base: [1] added b
  updating to "local" side of the conflict: 593c57f2117e
  merging "other" content-divergent changeset '8374d2ddc3a4'
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  working directory is now at 45bf1312f454
  $ hg log -G
  @  4:45bf1312f454@default(draft) divergent []
  |
  o  0:9092f1db7931@default(draft) added a []
  
Test divergence resolution when it yields to an empty commit (issue4950)
cdivergent2 contains the same content than cdivergent1 and they are divergent
versions of the revision _c

  $ hg up .^
  0 files updated, 0 files merged, 2 files removed, 0 files unresolved
  $ mkcommit _c
  created new head

  $ hg up .^
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ mkcommit cdivergent1
  created new head

  $ hg up .^
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ echo "cdivergent1" > cdivergent1
  $ hg add cdivergent1
  $ hg ci -m "add _c"
  created new head

  $ hg log -G
  @  7:b2ae71172042@default(draft) add _c []
  |
  | o  6:e3ff64ce8d4c@default(draft) add cdivergent1 []
  |/
  | o  5:48819a835615@default(draft) add _c []
  |/
  | o  4:45bf1312f454@default(draft) divergent []
  |/
  o  0:9092f1db7931@default(draft) added a []
  

  $ hg prune -s b2ae71172042 48819a835615
  1 changesets pruned
  $ hg prune -s e3ff64ce8d4c 48819a835615 --hidden
  1 changesets pruned
  2 new content-divergent changesets

  $ hg log -G
  @  7:b2ae71172042@default(draft) add _c [content-divergent]
  |
  | *  6:e3ff64ce8d4c@default(draft) add cdivergent1 [content-divergent]
  |/
  | o  4:45bf1312f454@default(draft) divergent []
  |/
  o  0:9092f1db7931@default(draft) added a []
  
  $ hg evolve --all --any --content-divergent
  merge:[6] add cdivergent1
  with: [7] add _c
  base: [5] add _c
  updating to "local" side of the conflict: e3ff64ce8d4c
  merging "other" content-divergent changeset 'b2ae71172042'
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  nothing changed
  working directory is now at e3ff64ce8d4c

  $ cd ..

Test None docstring issue of evolve divergent, which caused hg crush

  $ hg init test2
  $ cd test2
  $ mkcommits _a _b

  $ hg up .^
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ echo bdivergent > bdivergent11
  $ hg ci -Am "bdivergent"
  adding bdivergent11
  created new head

  $ hg up .^
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ echo bdivergent > bdivergent22
  $ hg ci -Am "bdivergent"
  adding bdivergent22
  created new head

  $ hg log -G
  @  3:6b096fb45070@default(draft) bdivergent []
  |
  | o  2:05a6b6a9e633@default(draft) bdivergent []
  |/
  | o  1:37445b16603b@default(draft) add _b []
  |/
  o  0:135f39f4bd78@default(draft) add _a []
  

  $ hg prune -s 6b096fb45070 37445b16603b
  1 changesets pruned
  $ hg prune -s 05a6b6a9e633 37445b16603b --hidden
  1 changesets pruned
  2 new content-divergent changesets
  $ hg log -G
  @  3:6b096fb45070@default(draft) bdivergent [content-divergent]
  |
  | *  2:05a6b6a9e633@default(draft) bdivergent [content-divergent]
  |/
  o  0:135f39f4bd78@default(draft) add _a []
  

  $ cat >$TESTTMP/test_extension.py  << EOF
  > from mercurial import merge
  > origupdate = merge.update
  > def newupdate(*args, **kwargs):
  >   return origupdate(*args, **kwargs)
  > merge.update = newupdate
  > EOF
  $ cat >> $HGRCPATH << EOF
  > [extensions]
  > testextension=$TESTTMP/test_extension.py
  > EOF
  $ hg evolve --all
  nothing to evolve on current working copy parent
  (do you want to use --content-divergent)
  [2]
  $ hg evolve --content-divergent
  merge:[3] bdivergent
  with: [2] bdivergent
  base: [1] add _b
  merging "other" content-divergent changeset '05a6b6a9e633'
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  working directory is now at 73ff357d3975

  $ cd ..
