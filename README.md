# Unmaintained

This project is currently looking for a maintainer! Please email `emacs@vimawesome.com` if you are interested.

The backend scraping/data pipeline is somewhat involved. Here's a [technical report on the details](https://www.dropbox.com/s/24owxihtek7vau9/report.pdf?dl=0). This was written for a school project in April 2014, and since then, there have been some minor changes to the backend code.

# Vim Awesome

Vim Awesome wants to be a comprehensive, accurate, and up-to-date directory of
Vim plugins.

Many recent Vim plugins are announced on Hacker News or specialized boards, and
have since become widely used. But how does a new user find out about these? We
wanted to solve that problem and others with Vim Awesome — an open-sourced
community resource for discovering new and popular Vim plugins.

## Where does the data come from?

GitHub, Vim.org, and user submissions.

On GitHub there are more than 30 000 repos that are development environment
configurations, commonly called dotfiles. From these repos we can extract
[references to Vim plugins (as Git URIs)](https://github.com/divad12/dotfiles/blob/master/.vimrc#L23),
particularly when plugin managers are used.

Although there are orders of magnitude more Vim users than public dotfiles
repos on GitHub, it is still a useful source of relative usage data.

## Getting set up

<!-- TODO(david): Don't hardcode version here. -->
1. Install RethinkDB version 1.16.1 from http://rethinkdb.com/docs/install/.
  (You may have to dig into the
  [download archives](http://download.rethinkdb.com/).)

1. Install Sass and Compass, which we use to generate our CSS.

  ```sh
  $ gem update --system
  $ gem install bundler
  $ bundle install
  ```

1. Install Python dependencies.

  ```sh
  $ pip install -r requirements.txt
  ```

1. Install Node dependencies.

  ```sh
  $ npm install -g webpack
  $ npm install
  ```

1. Start a local server serving port 5001 by invoking, in the project root
   directory,

  ```sh
  $ make
  ```

1. Initialize the database, tables, and indices:

  ```sh
  $ make init_db
  ```

1. Seed the database with some test data. Download [this database dump](https://dl.dropboxusercontent.com/u/18795947/rethinkdb_dump_2015-12-15.tar.gz), and then run

  ```sh
  $ rethinkdb restore -i vim_awesome /path/to/vim_awesome_rethinkdb_dump.tar.gz
  ```

1. Open the website in your browser!

  ```sh
  $ open http://localhost:5001
  ```

## Contributing

Take a look at [some of these issues](https://github.com/divad12/vim-awesome/issues?labels=easyfix&state=open) to get started.

Chat with us on #vimawesome on freenode!

## Acknowledgements

Thanks Ethan Schoonover for use of the Solarized colour scheme.

Much inspiration for this website, both conception and design, came from
[unheap.com](http://unheap.com), a resource for browsing jQuery plugins.

Built with [React](http://facebook.github.io/react/), a JavaScript library for
building UIs, and [RethinkDB](http://rethinkdb.com/), a document-oriented
database.
