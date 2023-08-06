** Test for handling of content divergent changesets by `hg evolve` **
====================================================================

  $ cat >> $HGRCPATH <<EOF
  > [alias]
  > glog = log -GT "{rev}:{node|short} {desc|firstline}\n ({bookmarks}) [{branch}] {phase}"
  > [phases]
  > publish = False
  > [extensions]
  > rebase =
  > EOF
  $ echo "evolve=$(echo $(dirname $TESTDIR))/hgext3rd/evolve/" >> $HGRCPATH

  $ hg init cdiv
  $ cd cdiv
  $ echo ".*\.orig" > .hgignore
  $ hg add .hgignore
  $ hg ci -m "added hgignore"
  $ for ch in a b c d; do echo foo > $ch; hg add $ch; hg ci -qm "added "$ch; done;

  $ hg glog
  @  4:c41c793e0ef1 added d
  |   () [default] draft
  o  3:ca1b80f7960a added c
  |   () [default] draft
  o  2:b1661037fa25 added b
  |   () [default] draft
  o  1:c7586e2a9264 added a
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

Creating content-divergence with branch change where base, divergent and other
have different branches
-------------------------------------------------------------------------------

  $ hg branch -r . foobar
  changed branch on 1 changesets

  $ hg up c41c793e0ef1 --hidden
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  updated to hidden changeset c41c793e0ef1
  (hidden revision 'c41c793e0ef1' was rewritten as: 9e5dffcb3d48)
  working directory parent is obsolete! (c41c793e0ef1)
  (use 'hg evolve' to update to its successor: 9e5dffcb3d48)
  $ echo bar > d
  $ hg branch watwat
  marked working directory as branch watwat
  $ hg amend
  2 new content-divergent changesets

  $ hg glog
  @  6:264b04f771fb added d
  |   () [watwat] draft
  | *  5:9e5dffcb3d48 added d
  |/    () [foobar] draft
  o  3:ca1b80f7960a added c
  |   () [default] draft
  o  2:b1661037fa25 added b
  |   () [default] draft
  o  1:c7586e2a9264 added a
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

  $ hg evolve --content-divergent --config ui.interactive=True<<EOF
  > c
  > EOF
  merge:[6] added d
  with: [5] added d
  base: [4] added d
  merging "other" content-divergent changeset '9e5dffcb3d48'
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  content divergent changesets on different branches.
  choose branch for the resolution changeset. (a) default or (b) watwat or (c) foobar?  c
  working directory is now at 0ac42f1bc15c

  $ hg glog
  @  7:0ac42f1bc15c added d
  |   () [foobar] draft
  o  3:ca1b80f7960a added c
  |   () [default] draft
  o  2:b1661037fa25 added b
  |   () [default] draft
  o  1:c7586e2a9264 added a
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

Testing merging of commit messages
-----------------------------------

When base and one of the divergent has same commit messages and other divergent
has different one

  $ echo wat > d
  $ hg amend

  $ hg up .^
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved

  $ echo bar > d
  $ hg ci -Aqm "added a d with bar in it, expect some beers"

  $ hg prune -r 0ac42f1bc15c -s . --hidden
  1 changesets pruned
  2 new content-divergent changesets

  $ hg glog
  @  9:59081c9c425a added a d with bar in it, expect some beers
  |   () [default] draft
  | *  8:f621d00f5f0e added d
  |/    () [foobar] draft
  o  3:ca1b80f7960a added c
  |   () [default] draft
  o  2:b1661037fa25 added b
  |   () [default] draft
  o  1:c7586e2a9264 added a
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

  $ hg evolve --content-divergent
  merge:[9] added a d with bar in it, expect some beers
  with: [8] added d
  base: [7] added d
  merging "other" content-divergent changeset 'f621d00f5f0e'
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  working directory is now at a9d6fd6b5e40

  $ hg glog
  @  10:a9d6fd6b5e40 added a d with bar in it, expect some beers
  |   () [default] draft
  o  3:ca1b80f7960a added c
  |   () [default] draft
  o  2:b1661037fa25 added b
  |   () [default] draft
  o  1:c7586e2a9264 added a
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

When base has different message and both divergents has same one

  $ echo foo > d
  $ hg amend -m "foo to d"

  $ hg up a9d6fd6b5e40 --hidden
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  updated to hidden changeset a9d6fd6b5e40
  (hidden revision 'a9d6fd6b5e40' was rewritten as: b10b07a394f1)
  working directory parent is obsolete! (a9d6fd6b5e40)
  (use 'hg evolve' to update to its successor: b10b07a394f1)
  $ echo babar > d
  $ hg amend -m "foo to d"
  2 new content-divergent changesets

  $ hg glog
  @  12:0bb497fed24a foo to d
  |   () [default] draft
  | *  11:b10b07a394f1 foo to d
  |/    () [default] draft
  o  3:ca1b80f7960a added c
  |   () [default] draft
  o  2:b1661037fa25 added b
  |   () [default] draft
  o  1:c7586e2a9264 added a
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

  $ hg evolve --content-divergent
  merge:[12] foo to d
  with: [11] foo to d
  base: [10] added a d with bar in it, expect some beers
  merging "other" content-divergent changeset 'b10b07a394f1'
  merging d
  warning: conflicts while merging d! (edit, then use 'hg resolve --mark')
  0 files updated, 0 files merged, 0 files removed, 1 files unresolved
  fix conflicts and see `hg help evolve.interrupted`
  [1]

  $ echo foobar > d
  $ hg resolve -m
  (no more unresolved files)
  continue: hg evolve --continue
  $ hg evolve --continue
  working directory is now at 11175423b5dc

  $ hg glog
  @  13:11175423b5dc foo to d
  |   () [default] draft
  o  3:ca1b80f7960a added c
  |   () [default] draft
  o  2:b1661037fa25 added b
  |   () [default] draft
  o  1:c7586e2a9264 added a
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

When all three base, divergent and other has different commit messages creating
conflicts

  $ echo bar > d
  $ hg amend -m "bar to d, expect beers"

  $ hg up 11175423b5dc --hidden
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  updated to hidden changeset 11175423b5dc
  (hidden revision '11175423b5dc' was rewritten as: 27f0463f169a)
  working directory parent is obsolete! (11175423b5dc)
  (use 'hg evolve' to update to its successor: 27f0463f169a)
  $ echo wat > d
  $ hg amend -m "wat to d, wat?"
  2 new content-divergent changesets

  $ hg glog
  @  15:f542037ddf31 wat to d, wat?
  |   () [default] draft
  | *  14:27f0463f169a bar to d, expect beers
  |/    () [default] draft
  o  3:ca1b80f7960a added c
  |   () [default] draft
  o  2:b1661037fa25 added b
  |   () [default] draft
  o  1:c7586e2a9264 added a
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

  $ hg evolve --content-divergent
  merge:[15] wat to d, wat?
  with: [14] bar to d, expect beers
  base: [13] foo to d
  merging "other" content-divergent changeset '27f0463f169a'
  merging d
  warning: conflicts while merging d! (edit, then use 'hg resolve --mark')
  0 files updated, 0 files merged, 0 files removed, 1 files unresolved
  fix conflicts and see `hg help evolve.interrupted`
  [1]

  $ echo watbar > d
  $ hg resolve -m
  (no more unresolved files)
  continue: hg evolve --continue

  $ cat > editor.sh <<EOF
  > #!/bin/sh
  > printf "**showing editors text**\n\n"
  > cat \$1
  > printf "\n**done showing editors text**\n\n"
  > cat > \$1 <<ENDOF
  > watbar to d
  > ENDOF
  > EOF

  $ HGEDITOR='sh ./editor.sh' hg evolve --continue
  **showing editors text**
  
  HG: Conflicts while merging changeset description of content-divergent changesets.
  HG: Resolve conflicts in commit messages to continue.
  
  <<<<<<< divergent
  wat to d, wat?||||||| base
  foo to d=======
  bar to d, expect beers>>>>>>> other
  
  **done showing editors text**
  
  working directory is now at 89ea3eee2d69

  $ hg glog
  @  16:89ea3eee2d69 watbar to d
  |   () [default] draft
  o  3:ca1b80f7960a added c
  |   () [default] draft
  o  2:b1661037fa25 added b
  |   () [default] draft
  o  1:c7586e2a9264 added a
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

  $ cd ..

Testing resolution of content-divergent changesets when they are on different
parents and resolution and relocation wont result in conflicts
------------------------------------------------------------------------------

  $ hg init multiparents
  $ cd multiparents
  $ echo ".*\.orig" > .hgignore
  $ hg add .hgignore
  $ hg ci -m "added hgignore"
  $ for ch in a b c d; do echo foo > $ch; hg add $ch; hg ci -qm "added "$ch; done;

  $ hg glog
  @  4:c41c793e0ef1 added d
  |   () [default] draft
  o  3:ca1b80f7960a added c
  |   () [default] draft
  o  2:b1661037fa25 added b
  |   () [default] draft
  o  1:c7586e2a9264 added a
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

  $ hg up .^^
  0 files updated, 0 files merged, 2 files removed, 0 files unresolved
  $ echo bar > b
  $ hg amend
  2 new orphan changesets

  $ hg rebase -r b1661037fa25 -d 8fa14d15e168 --hidden --config experimental.evolution.allowdivergence=True
  rebasing 2:b1661037fa25 "added b"
  2 new content-divergent changesets

  $ hg glog
  *  6:da4b96f4a8d6 added b
  |   () [default] draft
  | @  5:7ed0642d644b added b
  | |   () [default] draft
  | | *  4:c41c793e0ef1 added d
  | | |   () [default] draft
  | | *  3:ca1b80f7960a added c
  | | |   () [default] draft
  | | x  2:b1661037fa25 added b
  | |/    () [default] draft
  | o  1:c7586e2a9264 added a
  |/    () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

  $ hg evolve --content-divergent
  merge:[5] added b
  with: [6] added b
  base: [2] added b
  rebasing "other" content-divergent changeset da4b96f4a8d6 on c7586e2a9264
  updating to "local" side of the conflict: 7ed0642d644b
  merging "other" content-divergent changeset '11f849d7159f'
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  working directory is now at 171614c9a791

  $ hg glog
  @  8:171614c9a791 added b
  |   () [default] draft
  | *  4:c41c793e0ef1 added d
  | |   () [default] draft
  | *  3:ca1b80f7960a added c
  | |   () [default] draft
  | x  2:b1661037fa25 added b
  |/    () [default] draft
  o  1:c7586e2a9264 added a
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

  $ hg exp
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID 171614c9a7914c53f531373b95632323fdbbac8d
  # Parent  c7586e2a92645e473645847a7b69a6dc52be4276
  added b
  
  diff -r c7586e2a9264 -r 171614c9a791 b
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/b	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +bar

Resolving orphans to get back to a normal graph

  $ hg evolve --all
  move:[3] added c
  atop:[8] added b
  move:[4] added d
  working directory is now at 4ae4427ee9f8
  $ hg glog
  @  10:4ae4427ee9f8 added d
  |   () [default] draft
  o  9:917281f93fcb added c
  |   () [default] draft
  o  8:171614c9a791 added b
  |   () [default] draft
  o  1:c7586e2a9264 added a
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

More testing!

  $ hg up .^^
  0 files updated, 0 files merged, 2 files removed, 0 files unresolved
  $ echo x > x
  $ hg ci -Aqm "added x"
  $ hg glog -r .
  @  11:71a392c714b5 added x
  |   () [default] draft
  ~

  $ echo foo > x
  $ hg branch bar
  marked working directory as branch bar
  (branches are permanent and global, did you want a bookmark?)
  $ hg amend -m "added foo to x"

  $ hg up 71a392c714b5 --hidden
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  updated to hidden changeset 71a392c714b5
  (hidden revision '71a392c714b5' was rewritten as: 1e1a50385a7d)
  working directory parent is obsolete! (71a392c714b5)
  (use 'hg evolve' to update to its successor: 1e1a50385a7d)
  $ hg rebase -r . -d 4ae4427ee9f8 --config experimental.evolution.allowdivergence=True
  rebasing 11:71a392c714b5 "added x"
  2 new content-divergent changesets

  $ hg glog
  @  13:1e4f6b3bb39b added x
  |   () [default] draft
  | *  12:1e1a50385a7d added foo to x
  | |   () [bar] draft
  o |  10:4ae4427ee9f8 added d
  | |   () [default] draft
  o |  9:917281f93fcb added c
  |/    () [default] draft
  o  8:171614c9a791 added b
  |   () [default] draft
  o  1:c7586e2a9264 added a
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

  $ hg evolve --content-divergent
  merge:[13] added x
  with: [12] added foo to x
  base: [11] added x
  rebasing "other" content-divergent changeset 1e1a50385a7d on 4ae4427ee9f8
  updating to "local" side of the conflict: 1e4f6b3bb39b
  merging "other" content-divergent changeset '80cc9b1ec650'
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  working directory is now at b006cf317e0e

  $ hg exp
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Branch bar
  # Node ID b006cf317e0ed16dbe786c439577475580f645f1
  # Parent  4ae4427ee9f8f0935211fd66360948b77ab5aee9
  added foo to x
  
  diff -r 4ae4427ee9f8 -r b006cf317e0e x
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/x	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +foo

The above `hg exp` and the following log call demonstrates that message, content
and branch change is preserved in case of relocation
  $ hg glog
  @  15:b006cf317e0e added foo to x
  |   () [bar] draft
  o  10:4ae4427ee9f8 added d
  |   () [default] draft
  o  9:917281f93fcb added c
  |   () [default] draft
  o  8:171614c9a791 added b
  |   () [default] draft
  o  1:c7586e2a9264 added a
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

Testing when both the content-divergence are on different parents and resolution
will lead to conflicts
---------------------------------------------------------------------------------

  $ hg up .^^^
  0 files updated, 0 files merged, 3 files removed, 0 files unresolved

  $ echo y > y
  $ hg ci -Aqm "added y"
  $ hg glog -r .
  @  16:fc6ad2bac162 added y
  |   () [default] draft
  ~

  $ echo bar > y
  $ hg amend

  $ hg up fc6ad2bac162 --hidden
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  updated to hidden changeset fc6ad2bac162
  (hidden revision 'fc6ad2bac162' was rewritten as: 2a9f6ccbdeba)
  working directory parent is obsolete! (fc6ad2bac162)
  (use 'hg evolve' to update to its successor: 2a9f6ccbdeba)
  $ hg rebase -r . -d b006cf317e0e --config experimental.evolution.allowdivergence=True
  rebasing 16:fc6ad2bac162 "added y"
  2 new content-divergent changesets
  $ echo wat > y
  $ hg amend

  $ hg glog
  @  19:b4575ed6fcfc added y
  |   () [bar] draft
  | *  17:2a9f6ccbdeba added y
  | |   () [default] draft
  o |  15:b006cf317e0e added foo to x
  | |   () [bar] draft
  o |  10:4ae4427ee9f8 added d
  | |   () [default] draft
  o |  9:917281f93fcb added c
  |/    () [default] draft
  o  8:171614c9a791 added b
  |   () [default] draft
  o  1:c7586e2a9264 added a
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

  $ hg evolve --content-divergent
  merge:[19] added y
  with: [17] added y
  base: [16] added y
  rebasing "other" content-divergent changeset 2a9f6ccbdeba on b006cf317e0e
  updating to "local" side of the conflict: b4575ed6fcfc
  merging "other" content-divergent changeset '48f745db3f53'
  merging y
  warning: conflicts while merging y! (edit, then use 'hg resolve --mark')
  0 files updated, 0 files merged, 0 files removed, 1 files unresolved
  fix conflicts and see `hg help evolve.interrupted`
  [1]

  $ echo watbar > y
  $ hg resolve -m
  (no more unresolved files)
  continue: hg evolve --continue
  $ hg evolve --continue
  working directory is now at 7bbcf24ddecf

  $ hg glog
  @  21:7bbcf24ddecf added y
  |   () [bar] draft
  o  15:b006cf317e0e added foo to x
  |   () [bar] draft
  o  10:4ae4427ee9f8 added d
  |   () [default] draft
  o  9:917281f93fcb added c
  |   () [default] draft
  o  8:171614c9a791 added b
  |   () [default] draft
  o  1:c7586e2a9264 added a
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

  $ hg obslog -r . --all
  @    7bbcf24ddecf (21) added y
  |\
  x |  48f745db3f53 (20) added y
  | |    rewritten(branch, content) as 7bbcf24ddecf using evolve by test (Thu Jan 01 00:00:00 1970 +0000)
  | |
  | x  b4575ed6fcfc (19) added y
  | |    rewritten(content) as 7bbcf24ddecf using evolve by test (Thu Jan 01 00:00:00 1970 +0000)
  | |
  x |  2a9f6ccbdeba (17) added y
  | |    rewritten(parent) as 48f745db3f53 using evolve by test (Thu Jan 01 00:00:00 1970 +0000)
  | |
  | x  96b677f01b81 (18) added y
  |/     rewritten(content) as b4575ed6fcfc using amend by test (Thu Jan 01 00:00:00 1970 +0000)
  |
  x  fc6ad2bac162 (16) added y
       rewritten(content) as 2a9f6ccbdeba using amend by test (Thu Jan 01 00:00:00 1970 +0000)
       rewritten(branch, parent) as 96b677f01b81 using rebase by test (Thu Jan 01 00:00:00 1970 +0000)
  

checking that relocated commit is there
  $ hg exp 48f745db3f53 --hidden
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID 48f745db3f5300363ca248b9aeab20ff2a55fbb3
  # Parent  b006cf317e0ed16dbe786c439577475580f645f1
  added y
  
  diff -r b006cf317e0e -r 48f745db3f53 y
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/y	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +bar

Testing when the relocation will result in conflicts and merging wont
----------------------------------------------------------------------

  $ hg glog
  @  21:7bbcf24ddecf added y
  |   () [bar] draft
  o  15:b006cf317e0e added foo to x
  |   () [bar] draft
  o  10:4ae4427ee9f8 added d
  |   () [default] draft
  o  9:917281f93fcb added c
  |   () [default] draft
  o  8:171614c9a791 added b
  |   () [default] draft
  o  1:c7586e2a9264 added a
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

  $ hg up .^^^^
  0 files updated, 0 files merged, 4 files removed, 0 files unresolved

  $ echo z > z
  $ hg ci -Aqm "added z"
  $ hg glog -r .
  @  22:daf1de08f3b0 added z
  |   () [default] draft
  ~

  $ echo foo > y
  $ hg add y
  $ hg amend

  $ hg up daf1de08f3b0 --hidden
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  updated to hidden changeset daf1de08f3b0
  (hidden revision 'daf1de08f3b0' was rewritten as: 3f7a1f693080)
  working directory parent is obsolete! (daf1de08f3b0)
  (use 'hg evolve' to update to its successor: 3f7a1f693080)
  $ hg rebase -r . -d 7bbcf24ddecf --config experimental.evolution.allowdivergence=True
  rebasing 22:daf1de08f3b0 "added z"
  2 new content-divergent changesets
  $ echo bar > z
  $ hg amend

  $ hg glog
  @  25:53242575ffa9 added z
  |   () [bar] draft
  | *  23:3f7a1f693080 added z
  | |   () [default] draft
  o |  21:7bbcf24ddecf added y
  | |   () [bar] draft
  o |  15:b006cf317e0e added foo to x
  | |   () [bar] draft
  o |  10:4ae4427ee9f8 added d
  | |   () [default] draft
  o |  9:917281f93fcb added c
  |/    () [default] draft
  o  8:171614c9a791 added b
  |   () [default] draft
  o  1:c7586e2a9264 added a
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

  $ hg evolve --content-divergent
  merge:[25] added z
  with: [23] added z
  base: [22] added z
  rebasing "other" content-divergent changeset 3f7a1f693080 on 7bbcf24ddecf
  merging y
  warning: conflicts while merging y! (edit, then use 'hg resolve --mark')
  fix conflicts and see `hg help evolve.interrupted`
  [1]

  $ hg diff
  diff -r 7bbcf24ddecf y
  --- a/y	Thu Jan 01 00:00:00 1970 +0000
  +++ b/y	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,1 +1,5 @@
  +<<<<<<< destination: 7bbcf24ddecf bar - test: added y
   watbar
  +=======
  +foo
  +>>>>>>> evolving:    3f7a1f693080 - test: added z
  diff -r 7bbcf24ddecf z
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/z	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +z

  $ echo foo > y
  $ hg resolve -m
  (no more unresolved files)
  continue: hg evolve --continue

  $ hg evolve --continue
  evolving 23:3f7a1f693080 "added z"
  updating to "local" side of the conflict: 53242575ffa9
  merging "other" content-divergent changeset 'cdb0643c69fc'
  merging y
  warning: conflicts while merging y! (edit, then use 'hg resolve --mark')
  0 files updated, 0 files merged, 0 files removed, 1 files unresolved
  fix conflicts and see `hg help evolve.interrupted`
  [1]

  $ hg diff
  diff -r 53242575ffa9 y
  --- a/y	Thu Jan 01 00:00:00 1970 +0000
  +++ b/y	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,1 +1,5 @@
  +<<<<<<< local: 53242575ffa9 bar - test: added z
   watbar
  +=======
  +foo
  +>>>>>>> other: cdb0643c69fc - test: added z

  $ echo foo > y
  $ hg resolve -m
  (no more unresolved files)
  continue: hg evolve --continue
  $ hg evolve --continue
  working directory is now at 6fc7d9682de6

  $ hg glog
  @  27:6fc7d9682de6 added z
  |   () [bar] draft
  o  21:7bbcf24ddecf added y
  |   () [bar] draft
  o  15:b006cf317e0e added foo to x
  |   () [bar] draft
  o  10:4ae4427ee9f8 added d
  |   () [default] draft
  o  9:917281f93fcb added c
  |   () [default] draft
  o  8:171614c9a791 added b
  |   () [default] draft
  o  1:c7586e2a9264 added a
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

  $ hg exp
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Branch bar
  # Node ID 6fc7d9682de6e3bee6c8b1266b756ed7d522b7e4
  # Parent  7bbcf24ddecfe97d7c2ac6fa8c07c155c8fda47b
  added z
  
  diff -r 7bbcf24ddecf -r 6fc7d9682de6 y
  --- a/y	Thu Jan 01 00:00:00 1970 +0000
  +++ b/y	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,1 +1,1 @@
  -watbar
  +foo
  diff -r 7bbcf24ddecf -r 6fc7d9682de6 z
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/z	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +bar

  $ cd ..

Resolving content-divergence of a stack with same parents
---------------------------------------------------------

  $ hg init stacktest
  $ cd stacktest
  $ echo ".*\.orig" > .hgignore
  $ hg add .hgignore
  $ hg ci -m "added hgignore"
  $ for ch in a b c d; do echo foo > $ch; hg add $ch; hg ci -qm "added "$ch; done;

  $ hg glog
  @  4:c41c793e0ef1 added d
  |   () [default] draft
  o  3:ca1b80f7960a added c
  |   () [default] draft
  o  2:b1661037fa25 added b
  |   () [default] draft
  o  1:c7586e2a9264 added a
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

  $ cd ..
  $ hg init stack2
  $ cd stack2
  $ hg pull ../stacktest
  pulling from ../stacktest
  requesting all changes
  adding changesets
  adding manifests
  adding file changes
  added 5 changesets with 5 changes to 5 files
  new changesets 8fa14d15e168:c41c793e0ef1 (5 drafts)
  (run 'hg update' to get a working copy)
  $ hg glog
  o  4:c41c793e0ef1 added d
  |   () [default] draft
  o  3:ca1b80f7960a added c
  |   () [default] draft
  o  2:b1661037fa25 added b
  |   () [default] draft
  o  1:c7586e2a9264 added a
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

  $ hg up c7586e2a9264
  2 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ echo bar > a
  $ hg amend -m "watbar to a"
  3 new orphan changesets
  $ echo wat > a
  $ hg amend -m "watbar to a"
  $ hg evolve --all
  move:[2] added b
  atop:[6] watbar to a
  move:[3] added c
  move:[4] added d
  working directory is now at 15c781f93cac
  $ hg glog
  @  9:15c781f93cac added d
  |   () [default] draft
  o  8:9e5fb1d5b955 added c
  |   () [default] draft
  o  7:88516dccf68a added b
  |   () [default] draft
  o  6:82b74d5dc678 watbar to a
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

  $ cd ../stacktest
  $ hg up .^^^
  0 files updated, 0 files merged, 3 files removed, 0 files unresolved
  $ echo wat > a
  $ hg amend -m "watbar to a"
  3 new orphan changesets
  $ hg evolve --all
  move:[2] added b
  atop:[5] watbar to a
  move:[3] added c
  move:[4] added d
  working directory is now at c72d2885eb51
  $ hg glog
  @  8:c72d2885eb51 added d
  |   () [default] draft
  o  7:3ce4be6d8e5e added c
  |   () [default] draft
  o  6:d5f148423c16 added b
  |   () [default] draft
  o  5:8e222f257bbf watbar to a
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

  $ hg pull ../stack2
  pulling from ../stack2
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 4 changesets with 0 changes to 4 files (+1 heads)
  5 new obsolescence markers
  8 new content-divergent changesets
  new changesets 82b74d5dc678:15c781f93cac (4 drafts)
  (run 'hg heads' to see heads, 'hg merge' to merge)

  $ hg glog
  *  12:15c781f93cac added d
  |   () [default] draft
  *  11:9e5fb1d5b955 added c
  |   () [default] draft
  *  10:88516dccf68a added b
  |   () [default] draft
  *  9:82b74d5dc678 watbar to a
  |   () [default] draft
  | @  8:c72d2885eb51 added d
  | |   () [default] draft
  | *  7:3ce4be6d8e5e added c
  | |   () [default] draft
  | *  6:d5f148423c16 added b
  | |   () [default] draft
  | *  5:8e222f257bbf watbar to a
  |/    () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

  $ hg evolve --all --content-divergent
  merge:[5] watbar to a
  with: [9] watbar to a
  base: [1] added a
  updating to "local" side of the conflict: 8e222f257bbf
  merging "other" content-divergent changeset '82b74d5dc678'
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  6 new orphan changesets
  merge:[6] added b
  with: [10] added b
  base: [2] added b
  updating to "local" side of the conflict: d5f148423c16
  merging "other" content-divergent changeset '88516dccf68a'
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  merge:[7] added c
  with: [11] added c
  base: [3] added c
  updating to "local" side of the conflict: 3ce4be6d8e5e
  merging "other" content-divergent changeset '9e5fb1d5b955'
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  merge:[8] added d
  with: [12] added d
  base: [4] added d
  updating to "local" side of the conflict: c72d2885eb51
  merging "other" content-divergent changeset '15c781f93cac'
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  working directory is now at 038fe7db3d88

  $ hg glog
  @  16:038fe7db3d88 added d
  |   () [default] draft
  o  15:b2cac10f3836 added c
  |   () [default] draft
  o  14:eadfd9d70680 added b
  |   () [default] draft
  o  13:f66f262fff6c watbar to a
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft
