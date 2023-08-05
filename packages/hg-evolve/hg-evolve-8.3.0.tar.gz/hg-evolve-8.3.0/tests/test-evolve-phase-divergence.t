** Test for handling of phase divergent changesets by `hg evolve` **
====================================================================

  $ cat >> $HGRCPATH <<EOF
  > [alias]
  > glog = log -GT "{rev}:{node|short} {desc|firstline}\n ({bookmarks}) {phase}"
  > [extensions]
  > rebase =
  > EOF

Setting up a public repo
------------------------

  $ hg init public
  $ cd public
  $ echo a > a
  $ mkcommit() {
  >    echo "$1" > "$1"
  >    hg add "$1"
  >    hg ci -m "add $1"
  > }
  $ hg commit -A -m init
  adding a
  $ cd ..

  $ evolvepath=$(echo $(dirname $TESTDIR))/hgext3rd/evolve/

Setting up a private non-publishing repo
----------------------------------------

  $ hg clone -U public private
  $ cd private
  $ cat >> .hg/hgrc <<EOF
  > [extensions]
  > evolve = $evolvepath
  > [ui]
  > logtemplate = {rev}:{node|short}@{branch}({phase}) {desc|firstline}\n
  > [phases]
  > publish = false
  > EOF
  $ cd ..

Setting up couple of more instances of private repo
---------------------------------------------------

  $ cp -a private alice
  $ cp -a private bob

Creating a phase-divergence changeset
-------------------------------------

Alice creating a draft changeset and pushing to main private repo

  $ cd alice
  $ hg update
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ echo a >> a
  $ hg commit -u alice -m 'modify a'
  $ hg push ../private
  pushing to ../private
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files
  $ hg glog
  @  1:4d1169d82e47 modify a
  |   () draft
  o  0:d3873e73d99e init
      () public

Bob pulling from private repo and pushing to the main public repo making the
changeset public

  $ cd ../bob
  $ hg pull ../private
  pulling from ../private
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files
  new changesets 4d1169d82e47
  (run 'hg update' to get a working copy)

  $ hg glog
  o  1:4d1169d82e47 modify a
  |   () draft
  o  0:d3873e73d99e init
      () public

  $ hg push ../public
  pushing to ../public
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files

  $ hg glog
  o  1:4d1169d82e47 modify a
  |   () public
  o  0:d3873e73d99e init
      () public

*But* Alice decided to amend the changeset she had and then pulling from public
repo creating phase-divergent changeset locally

  $ cd ../alice
  $ hg amend -m 'tweak a'

XXX: pull should tell us how to see what is the new phase-divergent changeset
  $ hg pull ../public
  pulling from ../public
  searching for changes
  no changes found
  1 new phase-divergent changesets
  1 local changesets published

  $ hg glog
  @  2:98bb3a6cfe1a tweak a
  |   () draft
  | o  1:4d1169d82e47 modify a
  |/    () public
  o  0:d3873e73d99e init
      () public

Using evolve --list to list phase-divergent changesets
------------------------------------------------------

  $ hg evolve --list
  98bb3a6cfe1a: tweak a
    phase-divergent: 4d1169d82e47 (immutable precursor)
  


XXX-Pulkit: Trying to see instability on public changeset

XXX-Pulkit: this is not helpful

XXX-Marmoute: public changeset "instable themself"
XXX-Marmoute: I'm not sure if we store this information and it is useful to show it.
XXX-Marmoute: We should maybe point the user toward `hg obslog` instead`
  $ hg evolve -r 4d1169d8 --list
  4d1169d82e47: modify a
  

Understanding phasedivergence using obslog
------------------------------------------

XXX: There must be mention of phase-divergence here
  $ hg obslog -r . --all
  @  98bb3a6cfe1a (2) tweak a
  |
  o  4d1169d82e47 (1) modify a
       rewritten(description) as 98bb3a6cfe1a using amend by test (Thu Jan 01 00:00:00 1970 +0000)
  
Solving the phase divergence using evolve command
--------------------------------------------------

(We do not solve evolution other than orphan by default because it turned out
it was too confusing for users. We used to behave this way, but having multiple
possible outcome to evolve end up scaring people)

  $ hg evolve
  nothing to evolve on current working copy parent
  (do you want to use --phase-divergent)
  [2]

testing the --confirm option
  $ hg evolve --phase-divergent --confirm <<EOF
  > n
  > EOF
  recreate:[2] tweak a
  atop:[1] modify a
  perform evolve? [Ny] n
  abort: evolve aborted by user
  [255]

testing the --dry-run option

  $ hg evolve --phase-divergent --dry-run
  recreate:[2] tweak a
  atop:[1] modify a
  hg rebase --rev 98bb3a6cfe1a --dest d3873e73d99e;
  hg update 4d1169d82e47;
  hg revert --all --rev 98bb3a6cfe1a;
  hg commit --msg "phase-divergent update to 98bb3a6cfe1a"

XXX: evolve should have mentioned that draft commit is just obsoleted in favour
of public one. From the message it looks like a new commit is created.

  $ hg evolve --phase-divergent
  recreate:[2] tweak a
  atop:[1] modify a
  computing new diff
  committed as 4d1169d82e47
  working directory is now at 4d1169d82e47

  $ hg glog
  @  1:4d1169d82e47 modify a
  |   () public
  o  0:d3873e73d99e init
      () public

Syncying every repo with the new state
--------------------------------------

  $ hg push ../public
  pushing to ../public
  searching for changes
  no changes found
  2 new obsolescence markers
  [1]
  $ hg push ../private
  pushing to ../private
  searching for changes
  no changes found
  2 new obsolescence markers
  [1]
  $ hg push ../bob
  pushing to ../bob
  searching for changes
  no changes found
  2 new obsolescence markers
  [1]

Creating more phase-divergence where a new resolution commit will be formed and
also testing bookmark movement
--------------------------------------------------------------------------------

Alice created a commit and push to private non-publishing repo

  $ echo foo > foo
  $ hg add foo
  $ hg ci -m "added foo to foo"
  $ hg glog
  @  3:aa071e5554e3 added foo to foo
  |   () draft
  o  1:4d1169d82e47 modify a
  |   () public
  o  0:d3873e73d99e init
      () public

  $ hg push ../private
  pushing to ../private
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files

Bob pulled from the private repo and pushed that to publishing repo

  $ cd ../bob
  $ hg pull ../private
  pulling from ../private
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files
  new changesets aa071e5554e3
  (run 'hg update' to get a working copy)

  $ hg push ../public
  pushing to ../public
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files

Alice amended that changeset and then pulled from publishing repo creating
phase-divergence

  $ cd ../alice
  $ echo bar >> foo
  $ hg amend -m "added bar to foo"
  $ hg bookmark bm

  $ hg pull ../public
  pulling from ../public
  searching for changes
  no changes found
  1 new phase-divergent changesets
  1 local changesets published

  $ hg glog
  @  4:d47f2b37ed82 added bar to foo
  |   (bm) draft
  | o  3:aa071e5554e3 added foo to foo
  |/    () public
  o  1:4d1169d82e47 modify a
  |   () public
  o  0:d3873e73d99e init
      () public

Resolving the new phase-divergence changeset using `hg evolve`
--------------------------------------------------------------

XXX: this should have popped up for a new commit message of the changeset or an
option should be there

XXX: we should document what should user expect where running this, writing this
test I have to go through code base to understand what will be the behavior

  $ hg evolve --phase-divergent
  recreate:[4] added bar to foo
  atop:[3] added foo to foo
  computing new diff
  committed as 3d62500c673d
  working directory is now at 3d62500c673d

  $ hg exp
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID 3d62500c673dd1c88bb09a73e86d0210aed6fcb6
  # Parent  aa071e5554e36080a36cfd24accd5a71e3320f1e
  phase-divergent update to aa071e5554e3:
  
  added bar to foo
  
  diff -r aa071e5554e3 -r 3d62500c673d foo
  --- a/foo	Thu Jan 01 00:00:00 1970 +0000
  +++ b/foo	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,1 +1,2 @@
   foo
  +bar

XXX: the commit message is not best one, we should give option to user to modify
the commit message

  $ hg glog
  @  5:3d62500c673d phase-divergent update to aa071e5554e3:
  |   (bm) draft
  o  3:aa071e5554e3 added foo to foo
  |   () public
  o  1:4d1169d82e47 modify a
  |   () public
  o  0:d3873e73d99e init
      () public

  $ hg obslog -r . --all
  @  3d62500c673d (5) phase-divergent update to aa071e5554e3:
  |
  x  d47f2b37ed82 (4) added bar to foo
  |    rewritten(description, parent, content) as 3d62500c673d using evolve by test (Thu Jan 01 00:00:00 1970 +0000)
  |
  o  aa071e5554e3 (3) added foo to foo
       rewritten(description, content) as d47f2b37ed82 using amend by test (Thu Jan 01 00:00:00 1970 +0000)
  

Syncing all other repositories
------------------------------

These pushed should not be turned to quiet mode as the output is very helpful to
make sure everything is working fine

  $ hg push ../bob
  pushing to ../bob
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files
  2 new obsolescence markers

  $ hg push ../private
  pushing to ../private
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files
  2 new obsolescence markers

  $ hg push ../public
  pushing to ../public
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files
  2 new obsolescence markers

Creating a phasedivergence changeset where the divergent changeset changed in a
way that we rebase that on old public changeset, there will be conflicts, but
the `hg evolve` command handles it very well and uses `hg revert` logic to
prevent any conflicts
-------------------------------------------------------------------------------

Alice creates one more changeset and pushes to private repo

  $ echo bar > bar
  $ hg ci -Aqm "added bar to bar"
  $ hg push ../private
  pushing to ../private
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files

Bob pulls from private and pushes to public repo
  $ cd ../bob

  $ hg pull ../private
  pulling from ../private
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files
  new changesets b756eb10ea73
  1 local changesets published
  (run 'hg update' to get a working copy)

  $ hg push ../public
  pushing to ../public
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files

Alice amends the changeset and then pull from public creating phase-divergence

  $ cd ../alice
  $ echo foo > bar
  $ hg amend -m "foo to bar"

  $ hg pull ../public
  pulling from ../public
  searching for changes
  no changes found
  1 new phase-divergent changesets
  1 local changesets published

  $ hg glog
  @  7:2c3560aedead foo to bar
  |   (bm) draft
  | o  6:b756eb10ea73 added bar to bar
  |/    () public
  o  5:3d62500c673d phase-divergent update to aa071e5554e3:
  |   () public
  o  3:aa071e5554e3 added foo to foo
  |   () public
  o  1:4d1169d82e47 modify a
  |   () public
  o  0:d3873e73d99e init
      () public

Resolving the new phase-divergence changeset using `hg evolve`
---------------------------------------------------------------

  $ hg evolve --phase-divergent
  recreate:[7] foo to bar
  atop:[6] added bar to bar
  computing new diff
  committed as 502e73736632
  working directory is now at 502e73736632

  $ hg exp
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID 502e737366322886cf628276aa0a2796904453b4
  # Parent  b756eb10ea73ee4ba69c998e64a5c6e1005d74b5
  phase-divergent update to b756eb10ea73:
  
  foo to bar
  
  diff -r b756eb10ea73 -r 502e73736632 bar
  --- a/bar	Thu Jan 01 00:00:00 1970 +0000
  +++ b/bar	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,1 +1,1 @@
  -bar
  +foo

  $ hg glog
  @  8:502e73736632 phase-divergent update to b756eb10ea73:
  |   (bm) draft
  o  6:b756eb10ea73 added bar to bar
  |   () public
  o  5:3d62500c673d phase-divergent update to aa071e5554e3:
  |   () public
  o  3:aa071e5554e3 added foo to foo
  |   () public
  o  1:4d1169d82e47 modify a
  |   () public
  o  0:d3873e73d99e init
      () public

Syncing all the repositories
----------------------------

  $ hg push ../private
  pushing to ../private
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files
  2 new obsolescence markers
  $ hg push ../public
  pushing to ../public
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files
  2 new obsolescence markers

Creating phase-divergence with divergent changeset and precursor having
different parents
-----------------------------------------------------------------------

Alice creates a changeset and pushes to private repo

  $ echo x > x
  $ hg ci -Am "added x to x"
  adding x

  $ hg push ../private
  pushing to ../private
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files

Bob does what he always does, pull from private and push to public, he is acting
as a CI service

  $ cd ../bob
  $ hg pull ../private
  pulling from ../private
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 2 changesets with 2 changes to 2 files
  2 new obsolescence markers
  new changesets 502e73736632:2352021b3785
  (run 'hg update' to get a working copy)
  $ hg push ../public
  pushing to ../public
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 1 changesets with 1 changes to 1 files

Alice like always dont care about Bob existence and rebases her changeset and
then pull from public repo creating phase divergence

  $ cd ../alice
  $ hg rebase -r . -d .^^^
  rebasing 9:2352021b3785 "added x to x" (bm tip)

  $ hg pull ../public
  pulling from ../public
  searching for changes
  no changes found
  1 new phase-divergent changesets
  1 local changesets published

  $ hg obslog -r .
  @  334e300d6db5 (10) added x to x
  |
  o  2352021b3785 (9) added x to x
       rewritten(parent) as 334e300d6db5 using rebase by test (Thu Jan 01 00:00:00 1970 +0000)
  
  $ hg glog -r .^::
  @  10:334e300d6db5 added x to x
  |   (bm) draft
  | o  9:2352021b3785 added x to x
  | |   () public
  | o  8:502e73736632 phase-divergent update to b756eb10ea73:
  | |   () public
  | o  6:b756eb10ea73 added bar to bar
  |/    () public
  o  5:3d62500c673d phase-divergent update to aa071e5554e3:
  |   () public
  ~

Using `hg evolve` to resolve phase-divergence
---------------------------------------------

  $ hg evolve --phase-divergent
  recreate:[10] added x to x
  atop:[9] added x to x
  rebasing to destination parent: 502e73736632
  (leaving bookmark bm)
  computing new diff
  committed as 2352021b3785
  working directory is now at 2352021b3785

XXX: we should move bookmark here
  $ hg glog
  @  9:2352021b3785 added x to x
  |   (bm) public
  o  8:502e73736632 phase-divergent update to b756eb10ea73:
  |   () public
  o  6:b756eb10ea73 added bar to bar
  |   () public
  o  5:3d62500c673d phase-divergent update to aa071e5554e3:
  |   () public
  o  3:aa071e5554e3 added foo to foo
  |   () public
  o  1:4d1169d82e47 modify a
  |   () public
  o  0:d3873e73d99e init
      () public

  $ hg obslog -r . b1a0e143e32b --all --hidden
  x  b1a0e143e32b (11) added x to x
  |    pruned using evolve by test (Thu Jan 01 00:00:00 1970 +0000)
  |
  x  334e300d6db5 (10) added x to x
  |    rewritten(parent) as b1a0e143e32b using evolve by test (Thu Jan 01 00:00:00 1970 +0000)
  |
  @  2352021b3785 (9) added x to x
       rewritten(parent) as 334e300d6db5 using rebase by test (Thu Jan 01 00:00:00 1970 +0000)
  

  $ hg exp
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID 2352021b37851be226ebed109b0eb6eada918566
  # Parent  502e737366322886cf628276aa0a2796904453b4
  added x to x
  
  diff -r 502e73736632 -r 2352021b3785 x
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/x	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +x

Creating divergence with parent and content change both but not resulting in
conflicts
-----------------------------------------------------------------------------

Alice is tired of pushing and pulling and will create phase-divergence locally

  $ hg glog
  @  9:2352021b3785 added x to x
  |   (bm) public
  o  8:502e73736632 phase-divergent update to b756eb10ea73:
  |   () public
  o  6:b756eb10ea73 added bar to bar
  |   () public
  o  5:3d62500c673d phase-divergent update to aa071e5554e3:
  |   () public
  o  3:aa071e5554e3 added foo to foo
  |   () public
  o  1:4d1169d82e47 modify a
  |   () public
  o  0:d3873e73d99e init
      () public

  $ echo y > y
  $ echo foobar >> foo
  $ hg add y
  $ hg ci -m "y to y and foobar to foo"
  $ hg rebase -r . -d .^^^
  rebasing 12:dc88f5aa9bc9 "y to y and foobar to foo" (tip)

  $ echo foo > y
  $ hg amend

Alice making the old changeset public to have content-divergence

  $ hg phase -r dc88f5aa9bc9 --public --hidden
  1 new phase-divergent changesets
  $ hg glog
  @  14:13015a180eee y to y and foobar to foo
  |   () draft
  | o  12:dc88f5aa9bc9 y to y and foobar to foo
  | |   () public
  | o  9:2352021b3785 added x to x
  | |   (bm) public
  | o  8:502e73736632 phase-divergent update to b756eb10ea73:
  |/    () public
  o  6:b756eb10ea73 added bar to bar
  |   () public
  o  5:3d62500c673d phase-divergent update to aa071e5554e3:
  |   () public
  o  3:aa071e5554e3 added foo to foo
  |   () public
  o  1:4d1169d82e47 modify a
  |   () public
  o  0:d3873e73d99e init
      () public

  $ hg obslog -r .
  @  13015a180eee (14) y to y and foobar to foo
  |
  x  211ab84d1689 (13) y to y and foobar to foo
  |    rewritten(content) as 13015a180eee using amend by test (Thu Jan 01 00:00:00 1970 +0000)
  |
  o  dc88f5aa9bc9 (12) y to y and foobar to foo
       rewritten(parent) as 211ab84d1689 using rebase by test (Thu Jan 01 00:00:00 1970 +0000)
  
Resolving divergence using `hg evolve`
-------------------------------------

  $ hg evolve --phase-divergent
  recreate:[14] y to y and foobar to foo
  atop:[12] y to y and foobar to foo
  rebasing to destination parent: 2352021b3785
  computing new diff
  committed as 8c2bb6fb44e9
  working directory is now at 8c2bb6fb44e9

  $ hg exp
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID 8c2bb6fb44e9443c64b3a2a3d061272c8e25e6ce
  # Parent  dc88f5aa9bc90a6418899d267d9524205dfb429b
  phase-divergent update to dc88f5aa9bc9:
  
  y to y and foobar to foo
  
  diff -r dc88f5aa9bc9 -r 8c2bb6fb44e9 y
  --- a/y	Thu Jan 01 00:00:00 1970 +0000
  +++ b/y	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,1 +1,1 @@
  -y
  +foo

  $ hg glog
  @  16:8c2bb6fb44e9 phase-divergent update to dc88f5aa9bc9:
  |   () draft
  o  12:dc88f5aa9bc9 y to y and foobar to foo
  |   () public
  o  9:2352021b3785 added x to x
  |   (bm) public
  o  8:502e73736632 phase-divergent update to b756eb10ea73:
  |   () public
  o  6:b756eb10ea73 added bar to bar
  |   () public
  o  5:3d62500c673d phase-divergent update to aa071e5554e3:
  |   () public
  o  3:aa071e5554e3 added foo to foo
  |   () public
  o  1:4d1169d82e47 modify a
  |   () public
  o  0:d3873e73d99e init
      () public

Creating divergence with parent and content change both which results in
conflicts while rebasing on parent
-----------------------------------------------------------------------------

  $ echo l > l
  $ hg ci -Aqm "added l to l"
  $ hg rebase -r . -d .^^^^
  rebasing 17:f3794e5a91dc "added l to l" (tip)
  $ echo kl > l
  $ echo foo > x
  $ hg add x
  $ hg amend

  $ hg obslog -r .
  @  5fd38c0de46e (19) added l to l
  |
  x  2bfd56949cf0 (18) added l to l
  |    rewritten(content) as 5fd38c0de46e using amend by test (Thu Jan 01 00:00:00 1970 +0000)
  |
  x  f3794e5a91dc (17) added l to l
       rewritten(parent) as 2bfd56949cf0 using rebase by test (Thu Jan 01 00:00:00 1970 +0000)
  

  $ hg phase -r f3794e5a91dc --public --hidden
  1 new phase-divergent changesets

Resolution using `hg evolve --phase-divergent`
----------------------------------------------

  $ hg evolve --phase-divergent
  recreate:[19] added l to l
  atop:[17] added l to l
  rebasing to destination parent: 8c2bb6fb44e9
  merging x
  warning: conflicts while merging x! (edit, then use 'hg resolve --mark')
  fix conflicts and see `hg help evolve.interrupted`
  [1]

  $ hg diff
  diff -r 8c2bb6fb44e9 l
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/l	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +kl
  diff -r 8c2bb6fb44e9 x
  --- a/x	Thu Jan 01 00:00:00 1970 +0000
  +++ b/x	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,1 +1,5 @@
  +<<<<<<< destination: 8c2bb6fb44e9 - test: phase-divergent update to dc88f5aa9...
   x
  +=======
  +foo
  +>>>>>>> evolving:    5fd38c0de46e - test: added l to l

  $ echo foo > x

  $ hg resolve -m
  (no more unresolved files)
  continue: hg evolve --continue

  $ hg evolve --continue
  evolving 19:5fd38c0de46e "added l to l"
  computing new diff
  committed as e3090241a10c
  working directory is now at e3090241a10c

  $ hg glog
  @  21:e3090241a10c phase-divergent update to f3794e5a91dc:
  |   () draft
  o  17:f3794e5a91dc added l to l
  |   () public
  o  16:8c2bb6fb44e9 phase-divergent update to dc88f5aa9bc9:
  |   () public
  o  12:dc88f5aa9bc9 y to y and foobar to foo
  |   () public
  o  9:2352021b3785 added x to x
  |   (bm) public
  o  8:502e73736632 phase-divergent update to b756eb10ea73:
  |   () public
  o  6:b756eb10ea73 added bar to bar
  |   () public
  o  5:3d62500c673d phase-divergent update to aa071e5554e3:
  |   () public
  o  3:aa071e5554e3 added foo to foo
  |   () public
  o  1:4d1169d82e47 modify a
  |   () public
  o  0:d3873e73d99e init
      () public

  $ hg exp
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID e3090241a10c320b6132e4673915fd6b19c0de39
  # Parent  f3794e5a91dc1d4d36fee5c423386b19433a1f48
  phase-divergent update to f3794e5a91dc:
  
  added l to l
  
  diff -r f3794e5a91dc -r e3090241a10c l
  --- a/l	Thu Jan 01 00:00:00 1970 +0000
  +++ b/l	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,1 +1,1 @@
  -l
  +kl
  diff -r f3794e5a91dc -r e3090241a10c x
  --- a/x	Thu Jan 01 00:00:00 1970 +0000
  +++ b/x	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,1 +1,1 @@
  -x
  +foo

Creating phase divergence when couple of changesets are folded into one
------------------------------------------------------------------------

  $ hg glog -r .
  @  21:e3090241a10c phase-divergent update to f3794e5a91dc:
  |   () draft
  ~
  $ echo f > f
  $ hg ci -Aqm "added f"
  $ echo g > g
  $ hg ci -Aqm "added g"

  $ hg fold -r . -r .^ --exact
  2 changesets folded
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved

  $ hg evolve --list

  $ hg phase -r 428f7900a969 --public --hidden
  1 new phase-divergent changesets

  $ hg glog -r f3794e5a91dc::
  @  24:e450d05b7d27 added g
  |   () draft
  | o  23:428f7900a969 added g
  | |   () public
  | o  22:21ae52e414e6 added f
  |/    () public
  o  21:e3090241a10c phase-divergent update to f3794e5a91dc:
  |   () public
  o  17:f3794e5a91dc added l to l
  |   () public
  ~

  $ hg evolve --list
  e450d05b7d27: added g
    phase-divergent: 21ae52e414e6 (immutable precursor)
    phase-divergent: 428f7900a969 (immutable precursor)
  
Resolving phase divergence using `hg evolve`

  $ hg evolve --phase-divergent --all
  recreate:[24] added g
  atop:[23] added g
  rebasing to destination parent: 21ae52e414e6
  computing new diff
  committed as 428f7900a969
  working directory is now at 428f7900a969

  $ hg glog -r f3794e5a91dc::
  @  23:428f7900a969 added g
  |   () public
  o  22:21ae52e414e6 added f
  |   () public
  o  21:e3090241a10c phase-divergent update to f3794e5a91dc:
  |   () public
  o  17:f3794e5a91dc added l to l
  |   () public
  ~

When the public changesets is splitted causing phase-divergence
---------------------------------------------------------------

  $ echo m > m
  $ echo n > n
  $ hg ci -Aqm "added m and n"

  $ hg glog -r 21ae52e414e6::
  @  26:849cee0a874b added m and n
  |   () draft
  o  23:428f7900a969 added g
  |   () public
  o  22:21ae52e414e6 added f
  |   () public
  ~

  $ hg prev
  0 files updated, 0 files merged, 2 files removed, 0 files unresolved
  [23] added g
  $ echo m > m
  $ hg ci -Aqm "added m"
  $ echo n > n
  $ hg ci -Aqm "added n"

  $ hg glog -r 428f7900a969::
  @  28:63ccb8ea7cae added n
  |   () draft
  o  27:f313e2b90e70 added m
  |   () draft
  | o  26:849cee0a874b added m and n
  |/    () draft
  o  23:428f7900a969 added g
  |   () public
  ~

  $ hg prune -r 849cee0a874b --succ f313e2b90e70 --succ 63ccb8ea7cae --split
  1 changesets pruned

  $ hg phase -r 849cee0a874b --hidden --public
  2 new phase-divergent changesets

  $ hg glog -r 428f7900a969::
  @  28:63ccb8ea7cae added n
  |   () draft
  *  27:f313e2b90e70 added m
  |   () draft
  | o  26:849cee0a874b added m and n
  |/    () public
  o  23:428f7900a969 added g
  |   () public
  ~

  $ hg evolve --all --phase-divergent
  recreate:[27] added m
  atop:[26] added m and n
  computing new diff
  committed as 870e1c3eddc3
  1 new orphan changesets
  recreate:[28] added n
  atop:[26] added m and n
  rebasing to destination parent: 428f7900a969
  computing new diff
  committed as 154b0179fb9b
  working directory is now at 154b0179fb9b

XXX: this is messy, we should solve things in better way
  $ hg glog -r 428f7900a969:: --hidden
  @  31:154b0179fb9b phase-divergent update to 849cee0a874b:
  |   () draft
  | x  30:1ebf33547a82 added n
  | |   () draft
  +---o  29:870e1c3eddc3 phase-divergent update to 849cee0a874b:
  | |     () draft
  | | x  28:63ccb8ea7cae added n
  | | |   () draft
  | | x  27:f313e2b90e70 added m
  | |/    () draft
  o |  26:849cee0a874b added m and n
  |/    () public
  o  23:428f7900a969 added g
  |   () public
  ~

XXX: not sure this is the correct
  $ hg exp 154b0179fb9b
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID 154b0179fb9b53d2f853d6ba04740bb3d7a5cabe
  # Parent  849cee0a874be7c4e75dfacb5ad72aa5696951ba
  phase-divergent update to 849cee0a874b:
  
  added n
  
  diff -r 849cee0a874b -r 154b0179fb9b m
  --- a/m	Thu Jan 01 00:00:00 1970 +0000
  +++ /dev/null	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,1 +0,0 @@
  -m

XXX: not sure this is correct
  $ hg exp 870e1c3eddc3
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID 870e1c3eddc34cc475e8e13d2fe1934210c1937e
  # Parent  849cee0a874be7c4e75dfacb5ad72aa5696951ba
  phase-divergent update to 849cee0a874b:
  
  added m
  
  diff -r 849cee0a874b -r 870e1c3eddc3 n
  --- a/n	Thu Jan 01 00:00:00 1970 +0000
  +++ /dev/null	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,1 +0,0 @@
  -n

When the public changeset is splitted across various branches
--------------------------------------------------------------

  $ echo p > p
  $ echo q > q
  $ hg ci -Aqm "added p and q"

  $ hg prev
  0 files updated, 0 files merged, 2 files removed, 0 files unresolved
  [31] phase-divergent update to 849cee0a874b:
  $ echo p > p
  $ hg ci -Aqm "added p"
  $ hg prev
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  [31] phase-divergent update to 849cee0a874b:
  $ echo q > q
  $ hg ci -Aqm "added q"

  $ hg glog -r 154b0179fb9b::
  @  34:e046341aa97c added q
  |   () draft
  | o  33:6f8c250eecff added p
  |/    () draft
  | o  32:8a70f55b2af3 added p and q
  |/    () draft
  o  31:154b0179fb9b phase-divergent update to 849cee0a874b:
  |   () draft
  ~

  $ hg prune -r 8a70f55b2af3 --succ 6f8c250eecff --succ e046341aa97c --split
  1 changesets pruned

  $ hg phase -r 8a70f55b2af3 --public --hidden
  2 new phase-divergent changesets

  $ hg glog -r 154b0179fb9b::
  @  34:e046341aa97c added q
  |   () draft
  | *  33:6f8c250eecff added p
  |/    () draft
  | o  32:8a70f55b2af3 added p and q
  |/    () public
  o  31:154b0179fb9b phase-divergent update to 849cee0a874b:
  |   () public
  ~

  $ hg evolve --list
  6f8c250eecff: added p
    phase-divergent: 8a70f55b2af3 (immutable precursor)
  
  e046341aa97c: added q
    phase-divergent: 8a70f55b2af3 (immutable precursor)
  
  $ hg evolve --all --phase-divergent
  recreate:[33] added p
  atop:[32] added p and q
  computing new diff
  committed as f3e41d89b3c5
  recreate:[34] added q
  atop:[32] added p and q
  computing new diff
  committed as 605c306d4f87
  working directory is now at 605c306d4f87

  $ hg glog -r 154b0179fb9b:: --hidden
  @  36:605c306d4f87 phase-divergent update to 8a70f55b2af3:
  |   () draft
  | o  35:f3e41d89b3c5 phase-divergent update to 8a70f55b2af3:
  |/    () draft
  | x  34:e046341aa97c added q
  | |   () draft
  | | x  33:6f8c250eecff added p
  | |/    () draft
  o |  32:8a70f55b2af3 added p and q
  |/    () public
  o  31:154b0179fb9b phase-divergent update to 849cee0a874b:
  |   () public
  ~

XXX: not sure this is correct
  $ hg exp 605c306d4f87
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID 605c306d4f87fccfdb5e7dd1c750b6d4f813defb
  # Parent  8a70f55b2af35452916dc89401a5ecf6553646a5
  phase-divergent update to 8a70f55b2af3:
  
  added q
  
  diff -r 8a70f55b2af3 -r 605c306d4f87 p
  --- a/p	Thu Jan 01 00:00:00 1970 +0000
  +++ /dev/null	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,1 +0,0 @@
  -p

XXX: not sure this is correct
  $ hg exp f3e41d89b3c5
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID f3e41d89b3c5f6ee49ccc734045856d7b025f048
  # Parent  8a70f55b2af35452916dc89401a5ecf6553646a5
  phase-divergent update to 8a70f55b2af3:
  
  added p
  
  diff -r 8a70f55b2af3 -r f3e41d89b3c5 q
  --- a/q	Thu Jan 01 00:00:00 1970 +0000
  +++ /dev/null	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,1 +0,0 @@
  -q

Testing the evolution of a phase-divergent merge with no conflicts
------------------------------------------------------------------

  $ hg glog -r 154b0179fb9b::
  @  36:605c306d4f87 phase-divergent update to 8a70f55b2af3:
  |   () draft
  | o  35:f3e41d89b3c5 phase-divergent update to 8a70f55b2af3:
  |/    () draft
  o  32:8a70f55b2af3 added p and q
  |   () public
  o  31:154b0179fb9b phase-divergent update to 849cee0a874b:
  |   () public
  ~

  $ echo h > h
  $ hg ci -Aqm "added h"
  $ hg prev
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  [36] phase-divergent update to 8a70f55b2af3:
  $ echo i > i
  $ hg ci -Aqm "added i"
  $ hg merge -r ef8c23f37b55
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  (branch merge, don't forget to commit)
  $ hg ci -m "merge h and i"

  $ hg glog -r 605c306d4f87::
  @    39:12ebe0d625d7 merge h and i
  |\    () draft
  | o  38:9bb561db4230 added i
  | |   () draft
  o |  37:ef8c23f37b55 added h
  |/    () draft
  o  36:605c306d4f87 phase-divergent update to 8a70f55b2af3:
  |   () draft
  ~

  $ hg up ef8c23f37b55
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ hg merge -r 9bb561db4230
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  (branch merge, don't forget to commit)
  $ hg ci -m "merge h and i successor"
  created new head
  $ hg glog -r 605c306d4f87::
  @    40:d2aeda868461 merge h and i successor
  |\    () draft
  +---o  39:12ebe0d625d7 merge h and i
  | |/    () draft
  | o  38:9bb561db4230 added i
  | |   () draft
  o |  37:ef8c23f37b55 added h
  |/    () draft
  o  36:605c306d4f87 phase-divergent update to 8a70f55b2af3:
  |   () draft
  ~

  $ hg prune -r 12ebe0d625d7 --succ .
  1 changesets pruned

  $ hg phase 12ebe0d625d7 --hidden --public
  1 new phase-divergent changesets

Resolution of phase-divergent merge commit using `hg evolve`

XXX: we should handle phase-divergent merges
  $ hg evolve --phase-divergent
  skipping d2aeda868461 : we do not handle merge yet
