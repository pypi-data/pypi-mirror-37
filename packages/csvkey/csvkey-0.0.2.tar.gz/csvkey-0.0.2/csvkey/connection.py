import pandas as pd
import yaml, os


class Connection:

    def _append_conf(self, dct):
        if os.path.exists(self.CONF_PATH):
            with open(self.CONF_PATH, 'r') as f:
                conf = yaml.load(f)
        else:
            conf = dict()

        if self.CSV_NAME in conf.keys():
            raise ValueError('same csv name registered')

        conf[self.CSV_NAME] = dct
        with open(self.CONF_PATH, 'w') as fw:
            yaml.dump(conf, fw)

    def _read_conf(self):
        if not os.path.exists(self.CONF_PATH):
            raise ValueError('No configuration found')

        with open(self.CONF_PATH, 'r') as f:
            conf = yaml.load(f)[self.CSV_NAME]

        self.DTYPES = conf['DTYPES']
        self.PRIMARY = conf['PRIMARY']
        self.UNIQUE = conf['UNIQUE']
        self.NOTNULL = conf['NOTNULL']

    def _return_csv_conf(self):
        conf = dict()

        conf['DTYPES'] = self.df.dtypes.apply(str).to_dict()
        conf['PRIMARY'] = self.PRIMARY
        conf['UNIQUE'] = self.UNIQUE
        conf['NOTNULL'] = self.NOTNULL

        return conf

    def _check_primary_key(self):
        key_set = set([tuple(v) for i, v in self.df.loc[:, self.PRIMARY].iterrows()])

        if len(key_set) != len(self.df):
            raise ValueError('PRIMARY KEY duplicated')

    def _check_unique(self):
        rows = len(self.df)
        for k in self.UNIQUE:
            if len(set(self.df[k])) != rows:
                raise ValueError('duplicated in {0}'.format(k))

    def _check_notnull(self):
        for k in self.NOTNULL:
            if any(self.df[k].isna()):
                raise ValueError('NaN in {0}'.format(k))

    def _check(self):
        if self.PRIMARY:
            self._check_primary_key()

        if self.UNIQUE:
            self._check_unique()

        if self.NOTNULL:
            self._check_notnull()

    def _set_path(self, path, conf):
        self.CSV_PATH = path
        self.CSV_NAME = os.path.basename(path)
        self.CONF_PATH = os.path.join(os.path.dirname(path), conf)

    def initialize(self, df, path, primary=None, unique=None, notnull=None, conf='csv.conf'):
        """
        register pd.DataFrame as database

        parameter
        ---------
        df : pd.DataFrame
            database to register
        path : str
            where the CSV and associated configurations are generated
        primary : list or None
            keys treated as a primary key
        unique : list or None
            columns whose values must be unique
        notnull : list or None
            columns whose values must not be NaN
        conf : str
            file name of configurations
        """
        self._set_path(path, conf)
        self.PRIMARY = primary
        self.UNIQUE = unique
        self.NOTNULL = notnull
        self.df = df

        self._check()
        self._append_conf(self._return_csv_conf())
        self.commit(check=False)

    def connect(self, path, conf='csv.conf', check=False):
        """
        connect to a CSV file

        parameter
        ---------
        path : str
            refer to the CSV registered by Handler.initialize
        conf : str
            file name of configurations
        check : bool
            check whether the connected databse follows its configurations
        """
        self._set_path(path, conf)
        self._read_conf()

        self.df = pd.read_csv(self.CSV_PATH, header=0, index_col=False,
                              dtype=self.DTYPES)
        if check:
            self._check()

    def commit(self, check=True):
        """
        overwrite the CSV file with current database

        parameter
        ---------
        check : bool
            check whether the connected databse follows its configurations
        """
        if check:
            self._check()

        self.df.to_csv(self.CSV_PATH, header=True, index=False)
