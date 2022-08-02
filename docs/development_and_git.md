# Development cycle and using Git

| **What you need to know** |                                     |
|---------------------------|-------------------------------------|
| Essential:                | Opening a terminal on your computer |

This guide is targeted towards people who haven't used Git much or at all, or aren't confident when doing so. It's not a complete starter's guide to Git, but it should contain enough steps that you can follow it while developing. This guide will cover both people whose responsibility it is to maintain the website (HackSoc **committee** members) and **contributors** who aren't on the committee but would like to suggest changes or improvements. 


## 0. Prerequisites

You should only have to do these once per computer; once you've done them then you should be good to go for most Git projects.

### Installing Git

#### Windows
Download Git from [https://git-scm.com/downloads](https://git-scm.com/downloads)

#### MacOS
If you use Xcode, then you should have `git` already installed. 

If you have `homebrew` then you can use `brew install git`.

Otherwise, download the binary installer from [https://git-scm.com/download/mac](https://git-scm.com/download/mac).

#### Linux
Your package manger should provide `git`, for example `sudo apt-get install git` for Ubuntu. For other distributions of Linux, search `<your distro name> install git`

### Setting up GitHub
You don't need a GitHub account to download and fiddle with the website, but you will if you want to make changes by submitting a **pull request (PR)**. Once you've created a GitHub account you may find it helpful [connect to GitHub with SSH](https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh) to save a lot of re-typing your password.

## 1. Clone the repository

**Cloning** a repository downloads it from a **remote** (GitHub) into a folder on your computer so that you can work on it.

### Contributors only: Fork the repository
If you're not on the committee and haven't been given access to the [Contributors](https://github.com/orgs/HackSoc/teams/contributors) team, you'll need to **fork** the HackSoc repository so that you can work on your own copy. On the [repository page][repo], click the "Fork" button. This will create a new repository at `https://github.com/<yourname>/hacksoc.org` which you have full access to modify.

If you've done this step previously, then check on your repository page that it's up to date. When the `main` branch is selected (as default), you should see the message "The branch is even with HackSoc:main". Otherwise, click the "Fetch upstream" menu and select "Fetch and merge".

### Everyone: cloning
If you've setup SSH, then the command to type is:
```
git clone git@github.com:hacksoc/hacksoc.org
```
or
```
git clone git@github.com:yourname/hacksoc.org
```
if you forked the repository in the previous step.

Otherwise, to fork with HTTPS, the command is
```
git clone https://github.com/hacksoc/hacksoc.org
```
or 
```
git clone https://github.com/yourname/hacksoc.org
```
similarly.

### If you've clone the repository before
From **inside the repository folder**, run
```
git pull origin main
```
to ensure that your copy is up-to-date.

## 2. Creating a branch
Don't commit work onto the `main` branch, even if you're using a forked copy. Instead, create a new branch with a descriptive title. An example might be `2021-03-05_agm-results`, which is a branch with the AGM results around 05/03/2021. Including the year and month is usually more important than the day, especially as the work often takes more than a day or two to complete. To create a new branch and switch to it, type:
```
git checkout main
# ensure that we're on main before branching
git checkout -b 2021-09_your-feature-name
# -b creates a new branch, checkout switches to the new branch immediately
```

We are now on the new branch and ready to start work!

## 3. Make some changes
Consult the rest of the [documentation](./index.md) for how to make changes to the area that you want. Start small, and when you've finished one section, check it works!

## 4. Test it!
No matter what change you've made, build the website and check that it's applied, and hasn't broken anything else along the way

## 5. Go back and fix it

## 6. Format code and commit changes
Once that bit's working, now's a good time to commit your work. First run the code formatter:

```
black hacksoc_org/
# if you've got the venv activated already

venv/bin/black hacksoc_org/
# otherwise
```

Next, it's time to make a commit! A **commit** is like a checkpoint, so you can fearlessly make changes knowing that you can get back to the last time it was working.

### Add (stage) files
You can use `git status` to show you all the **unstaged** files (changed files but won't be committed) and **untracked** files (new files that also won't be committed). To turn these into **staged** files (that *will* be committed), use `git add`:

```
git add README.md
# add/stage a single file

git add docs/
# add/stage all the unstaged and untracked files in docs/
```

Run `git status` again and you should see everything is now staged. If it's not, keep adding files until everything you want to include in this commit is staged

### Committing
`git commit` will create a commit on your current branch (which should be the one you created earlier) in your local copy of the repository. Use `git commit -m "Your message here"` and include a descriptive message of what you changed or what you fixed. Note that running `git commit` by itself will open up a text editor for you to write a longer commit message. If you're using Windows, this should be Notepad. On MacOS and Linux, this might be the user-unfriendly `vi`. If you've never used `vi` or `vim`, we recommend running 

```
git config --global core.editor nano
```

before using `git commit` without `-m`. 

## 7. Make more changes
Keep making changes, testing, fixing, and committing until you think you're done.

## 8. Push commits
You can do this at any point. To push your changes from your local branch, to a branch of the same name on the **remote** (GitHub), run
```
git push -u origin 2021-09_your-feature-name
```
substituting `2021-09_your-feature-name` with your branch name (you can check this with `git status`). Once you've run this for the first time, you can just use `git push` with no additional arguments.

## 9. Making a pull request

Go to [Pull Requests](https://github.com/HackSoc/hacksoc.org/pulls) on the repository and click "New pull request".

### Committee 
Select your branch in the **compare** section and click "Create pull request"

### Contributors
First click "compare across forks", select your repository in the **head repository** section, and select your branch in the **compare** section to the right, then click "Create pull request".

### Writing the PR
Give your pull request a descriptive title that explains what it improves/fixes, then give more details in the large text field. It may also be relevant to justify decisions, and list any specific places that you'd like reviewers to check/give feedback on

If your PR is still in-progress but you'd like feedback at this stage, then click the arrow next to Create Pull request and select "create Draft pull request". It might be helpful to list what's still to do in your PR description; you can edit it as work progresses.

Make sure to apply the relevant labels on the right-hand side, the most helpful ones are:
 - **Content**: your PR changes the textual content on the website
   - eg. a news article or updating an event description
 - **Frontend**: your PR changes the HTML, CSS, or JS on the website
   - eg. fixing styles, changing the page template
 - **Backend**: your PR changes the way the website is built
   - eg. modifying the Python source

These will help reviewers know what kind of changes to expect and look for.

## 10. Getting reviewed
If you're on committee, it may be appropriate to assign another member for review if you've agreed this previously. Otherwise, reviewers usually get notified of a new pull request, and they should review it shortly. 

Your pull request may not be perfect, and might need some changes before it's merged by a reviewer. Pull requests on HackSoc repositories are covered by our [Code of Conduct](https://www.hacksoc.org/coc.html), and as such:
 - You are expected to abide by the Code of Conduct when writing and replying to a pull requests
 - You can expect others to abide by the Code of Conduct when replying to your pull request

If someone replies to you disrespectfully or in a manner that otherwise breaches the Code of Conduct, you can:
 - email hack@yusu.org
 - ping the @Committee role on Discord or direct message one of its members

## 11. Making changes from feedback
Once you've recieved feedback, you can follow the earlier steps: make changes, test, commit, push, and the new commit(s) will appear **in the same PR** &ndash; there's no need to delete your PR and create a new one. Once the reviewers are happy with your PR, they will merge it into the `main` branch.




[repo]: https://github.com/HackSoc/hacksoc.org
