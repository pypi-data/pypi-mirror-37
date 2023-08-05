from abc import ABCMeta, abstractmethod, abstractproperty


class Channel(metaclass=ABCMeta):
    """ Define the interface to all channels. Channels are usually called via the execute_wait function.
    For channels that execute remotely, a push_file function allows you to copy over files.

    .. code:: python

                                +------------------
                                |
          cmd, wtime    ------->|  execute_wait
          (ec, stdout, stderr)<-|---+
                                |
          cmd, wtime    ------->|  execute_no_wait
          (ec, stdout, stderr)<-|---+
                                |
          src, dst_dir  ------->|  push_file
             dst_path  <--------|----+
                                |
          dst_script_dir <------|  script_dir
                                |
                                +-------------------

    """

    @abstractmethod
    def execute_wait(self, cmd, walltime, envs={}, *args, **kwargs):
        ''' Executes the cmd, with a defined walltime.

        Args:
            - cmd (string): Command string to execute over the channel
            - walltime (int) : Timeout in seconds

        KWargs:
            - envs (dict) : Environment variables to push to the remote side

        Returns:
            - (exit_code, stdout, stderr) (int, string, string)
        '''
        pass

    @abstractproperty
    def script_dir(self):
        ''' This is a property. Returns the directory assigned for storing all internal scripts such as
        scheduler submit scripts. This is usually where error logs from the scheduler would reside on the
        channel destination side.

        Args:
            - None

        Returns:
            - Channel script dir
        '''
        pass

    @abstractmethod
    def execute_no_wait(self, cmd, walltime, envs={}, *args, **kwargs):
        ''' Optional. THis is infrequently used.

        Args:
            - cmd (string): Command string to execute over the channel
            - walltime (int) : Timeout in seconds

        KWargs:
            - envs (dict) : Environment variables to push to the remote side

        Returns:
            - (exit_code(None), stdout, stderr) (int, io_thing, io_thing)
        '''
        pass

    @abstractmethod
    def push_file(self, source, dest_dir):
        ''' Channel will take care of moving the file from source to the destination
        directory

        Args:
            source (string) : Full filepath of the file to be moved
            dest_dir (string) : Absolute path of the directory to move to

        Returns:
            destination_path (string)
        '''
        pass

    @abstractmethod
    def close(self):
        ''' Closes the channel. Clean out any auth credentials.

        Args:
            None

        Returns:
            Bool

        '''
        pass

    @abstractmethod
    def makedirs(self, path, mode=511, exist_ok=False):
        """Create a directory.

        If intermediate directories do not exist, they will be created.

        Parameters
        ----------
        path : str
            Path of directory to create.
        mode : int
            Permissions (posix-style) for the newly-created directory.
        exist_ok : bool
            If False, raise an OSError if the target directory already exists.
        """
        pass

    @abstractmethod
    def isdir(self, path):
        """Return true if the path refers to an existing directory.

        Parameters
        ----------
        path : str
            Path of directory to check.
        """
        pass

    @abstractmethod
    def abspath(self, path):
        """Return the absolute path.

        Parameters
        ----------
        path : str
            Path for which the absolute path will be returned.
        """
        pass

    @property
    def script_dir(self):
        return self._script_dir

    @script_dir.setter
    def script_dir(self, value):
        if value is not None:
            value = self.abspath(value)
        self._script_dir = value
