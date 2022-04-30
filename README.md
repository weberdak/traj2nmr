# Traj2NMR (Documentation Branch)

Dedicated branch to maintain documentation hosted by GitHub Pages


## Guide


### Initial setup

Clone repository and change branch:

    $ git clone https://github.com/weberdak/traj2nmr
    $ git checkout gh-pages

Setup Sphinx:

    $ pip install -r requirements.txt


### Making edits

Edit .rst files in the docs/source directory. Once complete, run the following in the docs directory:

    $ make html


### Committing changes

Add, commit and push to repo:

    $ git add docs
    $ git commit -m "Made some changes"
    $ git push origin gh-pages

