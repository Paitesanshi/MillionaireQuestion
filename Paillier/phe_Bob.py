import Paillier as pai
class Phe_Bob:

    def __init__(self, p:pai):
        self.x = p.__get_random__(100)
        self.y = p.__get_random__(128)
        self.wealth = 0

    # def encrypt_weights(self,model):
    #     coef = model.coef_[0, :]
    #     #print(coef.shape)
    #     #print(model.intercept_)
    #     encrypted_weights = [self.pubkey.encrypt(coef[i])
    #                          for i in range(coef.shape[0])]
    #     encrypted_intercept = self.pubkey.encrypt(model.intercept_[0])
    #     return encrypted_weights, encrypted_intercept

    # def decrypt_scores(self, encrypted_scores):
    #     return [self.privkey.decrypt(s) for s in encrypted_scores]
    def __set_wealth__(self,w):
        self.wealth=w
    def getPubkey(self):
        return self.pubkey

    def getPrivkey(self):
        return self.privkey
    def getWealth(self):
        return self.wealth
    def getX(self):
        return self.x
    def getY(self):
        return self.y

