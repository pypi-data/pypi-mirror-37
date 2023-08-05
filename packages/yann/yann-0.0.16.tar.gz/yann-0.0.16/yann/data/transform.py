from torchvision import transforms


def mixup(x1, x2, y1, y2, alpha=.5):
  pass



class Transformer:
  def __init__(self, load=None, transform=None, to_tensor=None):
    self.load = load
    self.transform = transform
    self.to_tensor = to_tensor

  def __call__(self, x):
    x = self.load(x)
    x = self.transform(x)
    return self.to_tensor(x)

  def prep(self, x):
    return self.transform(self.load(x))