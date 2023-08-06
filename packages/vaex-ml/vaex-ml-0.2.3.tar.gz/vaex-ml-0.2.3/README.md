Installation
 * Install [vaex](https://github.com/maartenbreddels/vaex) in dev mode
   * 'Trick' to get all vaex deps:
     * `$ conda install -c conda-forge vaex`
     * `$ conda uninstall vaex`
   * `$ git clone https://github.com/maartenbreddels/vaex`
   * `$ cd vaex`
   * `$ pip install -e . `
   * `$ cd ..`
 * Get 'our' xgboost
   * `git clone --recursive git@gitlab.com:maartenbreddels/xgboost.git`
   * `cd xgboost; make -j8`
     * for OSX possibly get a modern gcc from brew:
        *  `brew install --overwrite gcc --without-multilib`
        *  `export CXX=/usr/local/Cellar/gcc/7.2.0/bin/g++-7` (or whatever the path is that bew installed to)
        *  `export CC=/usr/local/Cellar/gcc/7.2.0/bin/gcc-7`
     * if installing on Mac OS X, you may need this:  `cd xgboost; cp make/minimum_parallel.mk ./config.mk; make -j8`
   * cd python-package
   * pip install -e .
   * cd ../..
 * Add vaex-ml to the vaex tree
  * cd vaex-ml
  * ln -s vaex/ml \`python -c 'import os,vaex as m; print(os.path.dirname(m.\__file\__))'\`/ml
  * To test: `python -m vaex.ml.xgboost iris.hdf5`