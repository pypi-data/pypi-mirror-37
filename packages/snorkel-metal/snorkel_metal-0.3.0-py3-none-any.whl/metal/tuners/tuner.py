import json
import os
import pickle
import random
from itertools import cycle, product
from time import strftime, time

import numpy as np


class ModelTuner(object):
    """A tuner for models

    Args:
        model: (nn.Module) The model class to train (uninitiated)
        log_dir: (str) The path to the base log directory, or defaults to
            current working directory.
        run_dir: (str) The name of the sub-directory, or defaults to the date,
            strftime("%Y_%m_%d").
        run_name: (str) The name of the run, or defaults to the time,
            strftime("%H_%M_%S").
        log_writer_class: a metal.utils.LogWriter class for logging the full
            model search.

        Saves current best model to 'log_dir/run_dir/{run_name}_best_model.pkl'.
    """

    def __init__(
        self,
        model_class,
        log_dir=None,
        run_dir=None,
        run_name=None,
        log_writer_class=None,
        seed=None,
    ):
        self.model_class = model_class
        self.log_writer_class = log_writer_class

        # Set logging subdirectory + make sure exists
        log_dir = log_dir or os.getcwd()
        run_dir = run_dir or strftime("%Y_%m_%d")
        log_subdir = os.path.join(log_dir, run_dir)
        if not os.path.exists(log_subdir):
            os.makedirs(log_subdir)

        # Set JSON log path
        run_name = run_name or strftime("%H_%M_%S")
        self.save_path = os.path.join(log_subdir, f"{run_name}_best_model.pkl")
        self.report_path = os.path.join(log_subdir, f"{run_name}_report.json")

        # Set global seed
        if seed is None:
            self.seed = 0
        else:
            random.seed(seed)
            self.seed = seed

        # Search state
        # NOTE: Must be cleared each run with self._clear_state()!
        self._clear_state()

    def _clear_state(self):
        """Clears the state, starts clock"""
        self.start_time = time()
        self.run_stats = []
        self.best_index = -1
        self.best_score = -1
        self.best_config = None

        # Note: These must be set at the start of self.search()
        self.search_space = None

    def _test_model_config(
        self,
        idx,
        config,
        dev_data,
        init_args=[],
        train_args=[],
        init_kwargs={},
        train_kwargs={},
        verbose=False,
        **score_kwargs,
    ):
        # Init model
        model = self.model_class(*init_args, **init_kwargs, **config)

        # Search params
        # Select any params in search space that have list or dict
        search_params = {
            k: v
            for k, v in config.items()
            if isinstance(self.search_space[k], (list, dict))
        }
        if verbose:
            print("=" * 60)
            print(f"[{idx}] Testing {search_params}")
            print("=" * 60)

        # Initialize a new LogWriter and train the model, returning the score
        log_writer = None
        if self.log_writer_class is not None:
            log_writer = self.log_writer_class(
                self.log_dir, run_name=f"model_search_{idx}"
            )
        model.train_model(
            *train_args,
            **train_kwargs,
            dev_data=dev_data,
            verbose=verbose,
            log_writer=log_writer,
            **config,
        )
        score = model.score(dev_data, verbose=verbose, **score_kwargs)

        # If score better than best_score, save
        if score > self.best_score:
            self.best_score = score
            self.best_index = idx
            self.best_config = config
            self._save_best_model(model)

        # Save high-level run stats (in addition to per-model log)
        time_elapsed = time() - self.start_time
        self.run_stats.append(
            {
                "idx": idx,
                "time_elapsed": time_elapsed,
                "search_params": search_params,
                "score": score,
            }
        )
        return score, model

    def _save_best_model(self, model):
        with open(self.save_path, "wb") as f:
            pickle.dump(model, f)

    def _load_best_model(self, clean_up=False):
        with open(self.save_path, "rb") as f:
            model = pickle.load(f)
        if clean_up:
            self._clean_up()
        return model

    def _clean_up(self):
        if os.path.exists(self.save_path):
            os.remove(self.save_path)

    def _save_report(self):
        with open(self.report_path, "wb") as f:
            json.dump(self.run_stats, f, indent=1)

    def search(
        self,
        search_space,
        dev_data,
        init_args=[],
        train_args=[],
        init_kwargs={},
        train_kwargs={},
        max_search=None,
        shuffle=True,
        verbose=True,
        **score_kwargs,
    ):
        """
        Args:
            search_space: see config_generator() documentation
            dev_data: a tuple of Tensors (X,Y), a Dataset, or a DataLoader of
                X (data) and Y (labels) for the dev split
            init_args: (list) positional args for initializing the model
            train_args: (list) positional args for training the model
            init_kwargs: (dict) keyword args for initializing the model
            train_kwargs: (dict) keyword args for training the model
            max_search: see config_generator() documentation
            shuffle: see config_generator() documentation
        Returns:
            best_model: the highest performing trained model

        Note: Initialization is performed by ModelTuner instead of passing a
        pre-initialized model so that tuning may be performed over all model
        parameters, including the network architecture (which is defined before
        the train loop).
        """
        raise NotImplementedError()

    @staticmethod
    def config_generator(search_space, max_search, shuffle=True):
        """Generates config dicts from the given search space

        Args:
            search_space: (dict) A dictionary of parameters to search over.
                See note below for more details.
            max_search: (int) The maximum number of configurations to search.
                If max_search is None, do a full grid search of all discrete
                    parameters, filling in range parameters as needed.
                Otherwise, do a full grid search of all discrete
                    parameters and then cycle through again filling in new
                    range parameters values; if there are no range parameters,
                    stop after yielding the full cross product of parameters
                    once.
            shuffle: (bool) If True, shuffle the order of generated configs

        Yields:
            configs: each config is a dict of parameter values based on the
                provided search space

        The search_space dictionary may consist of two types of parameters:
            --discrete: a discrete parameter is either a single value or a
                list of values. Use single values, for example, to override
                a default model parameter or set a flag such as 'verbose'=True.
            --range: a range parameter is a dict of the form:
                {'range': [<min>, <max>], 'scale': <scale>}
                where <min> and <max> are the min/max values to search between
                and scale is one of ['linear', 'log'] (defaulting to 'linear')
                representing the scale to use when searching the given range

        Example:
            search_space = {
                'verbose': True,                              # discrete
                'n_epochs': 100,                              # discrete
                'momentum': [0.0, 0.9, 0.99],                       # discrete
                'l2': {'range': [0.0001, 10]}                 # linear range
                'lr': {'range': [0.001, 1], 'scale': 'log'},  # log range
            }
            If max_search is None, this will return 3 configurations (enough to
                just cover the full cross-product of discrete values, filled
                in with sampled range values)
            Otherewise, this will return max_search configurations
                (cycling through the discrete value combinations multiple
                time if necessary)
        """

        def dict_product(d):
            keys = d.keys()
            for element in product(*d.values()):
                yield dict(zip(keys, element))

        def range_param_func(v):
            scale = v.get("scale", "linear")
            mini = min(v["range"])
            maxi = max(v["range"])
            if scale == "linear":
                func = lambda rand: mini + (maxi - mini) * rand
            elif scale == "log":
                mini = np.log(mini)
                maxi = np.log(maxi)
                func = lambda rand: np.exp(mini + (maxi - mini) * rand)
            else:
                raise ValueError(
                    f"Unrecognized scale '{scale}' for " "parameter {k}"
                )
            return func

        discretes = {}
        ranges = {}
        for k, v in search_space.items():
            if isinstance(v, dict):
                ranges[k] = range_param_func(v)
            elif isinstance(v, list):
                discretes[k] = v
            else:
                discretes[k] = [v]

        discrete_configs = list(dict_product(discretes))

        if shuffle:
            random.shuffle(discrete_configs)

        # If there are range parameters and a non-None max_search, cycle
        # through the discrete_configs (with new range values) until
        # max_search is met
        if ranges and max_search:
            discrete_configs = cycle(discrete_configs)

        for i, config in enumerate(discrete_configs):
            # We may see the same config twice due to cycle
            config = config.copy()
            if max_search and i == max_search:
                break
            for k, v in ranges.items():
                config[k] = float(v(random.random()))
            yield config
