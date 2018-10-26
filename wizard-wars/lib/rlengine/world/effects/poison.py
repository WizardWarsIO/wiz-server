from effect import * 

class PoisonEffect(Effect):
  def configure(self, params):
    super(PoisonEffect, self).configure(params)

    if 'original' in params.keys():
      self.original = params['original']
    else:
      self.original = self

  def getRendercode(self):
    return 500

  def effectType(self):
    return "poison"

  def spreadDelay(self):
    return 4