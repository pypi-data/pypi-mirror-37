import torch
import torch.utils.data

from .utils import memoize


class SafeDataset(torch.utils.data.Dataset):
    """A wrapper around a torch.utils.data.Dataset that allows dropping
    samples dynamically.
    """

    def __init__(self, dataset, eager_eval=False):
        """Creates a `SafeDataset` wrapper around `dataset`."""
        self.eager_eval = eager_eval
        # "Backup" of dataset's original __getitem__ function (since we will
        # be overwriting it)
        self._get_sample_original = dataset.__getitem__
        # _safe_get_item returns None instead of throwing an error when
        # dealing with a unsafe sample, and also builds an index of safe and
        # unsafe samples as it goes
        dataset.__class__.__getitem__ = self._safe_get_item
        self.dataset = dataset

        self.safe_samples_indices = []
        self.unsafe_samples_indices = []

        # If eager_eval is False, we can simply go ahead and build the index
        # by attempting to access every sample in self.dataset.
        if self.eager_eval is True:
            self._build_index()

    def _safe_get_item(self, idx):
        """Returns None instead of throwing an error when dealing with an
        unsafe sample, and also builds an index of safe and unsafe samples as
        and when they get accessed.
        """
        try:
            sample = self._get_sample_original(idx)
            if idx not in self.safe_samples_indices:
                self.safe_samples_indices.append(idx)
            return sample
        except IndexError: raise
        except Exception:
            if idx not in self.unsafe_samples_indices:
                self.unsafe_samples_indices.append(idx)
            return None

    def _build_index(self):
        for idx in range(len(self.dataset)):
            # The returned sample is deliberately discarded because
            # self.dataset[idx] is called only to classify every index
            # into either safe_samples_indices or unsafe_samples_indices.
            _ = self.dataset[idx]

    def _reset_index(self):
        """Resets the safe and unsafe samples indices."""
        self.safe_samples_indices = self.unsafe_samples_indices = []

    @property
    def is_index_built(self):
        """Returns True if all indices of the original dataset have been
        classified into safe_samples_indices or unsafe_samples_indices.
        """
        return len(self.dataset) == len(self.safe_samples_indices) + \
            len(self.unsafe_samples_indices)

    def __len__(self):
        """Returns the length of the original dataset.
        NOTE: This is different from the number of actually valid samples.
        """
        return len(self.dataset)

    def __iter__(self):
        return (self.dataset[i] for i in range(len(self.dataset)))

    @memoize
    def __getitem__(self, idx):
        """Behaves like the standard __getitem__ for Dataset when the index
        has been built.
        """
        if not self.is_index_built:
            raise RuntimeError('Index of safe samples is not yet built. ' +
                               'You can use this Dataset as an iterator. ' +
                               'However, you will not be able to index ' +
                               'arbitrary elements.')
        dataset_idx = self.safe_samples_indices[idx]
        return self.dataset[dataset_idx]
