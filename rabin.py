from typing import Optional


class RabinSystem():

    @staticmethod
    def encrypt(M: int, N: int) -> int:
        return M ** 2 % N

    @staticmethod
    def decrypt(
        enc: Optional[str],
        P: int, Q: int, N: int,
    ) -> Optional[str]:
        fit = 128
        P_1 = RabinSystem.balance_chinese(
            K=(P + 1) / 4,
            B=enc,
            M=P,
        )
        Q_1 = RabinSystem.balance_chinese(
            K=(Q + 1) / 4,
            B=enc,
            M=Q,
        )
        euclid = RabinSystem.euclid(P, Q)
        param_sum = euclid[0] * P * Q_1 + euclid[1] * Q * P_1
        param_diff = euclid[0] * P * Q_1 - euclid[1] * Q * P_1
        module = RabinSystem.module(param_sum, N)
        if module < fit:
            return module
        dif_module = N - module
        if dif_module < fit:
            return dif_module
        X = RabinSystem.module(param_diff, N)
        if X < fit:
            return X
        dif_X = N - X
        return dif_X

    @staticmethod
    def balance_chinese(K: int, B: int, M: int) -> int:
        idx = 0
        A = 1
        temp = []
        while K > 0:
            temp.append(K % 2)
            K = (K - temp[idx]) / 2
            idx += 1
        for j in range(idx):
            if temp[j] == 1:
                A = (A * B) % M
            B = (B * B) % M
        return A
    
    @staticmethod
    def module(X: int, Y: int) -> int:
        return X % Y if X >= 0 \
            else (Y - abs(X % Y)) % Y

    @staticmethod
    def euclid(X: int, Y: int) -> list:
        if Y > X: X, Y = Y, X
        a, b, x_1, y_1 = 0, 1, 1, 0
        while Y != 0:
            Q = int(X / Y)
            X, Y = Y, int(X % Y)
            x_1, a = a, int(x_1 - Q * a)
            y_1, b = b, int(y_1 - Q * b)
        return [x_1, y_1, 1]


class RabinCypher(RabinSystem):
    def __init__(self) -> None:
        self.P = int(input('Введіть значення P: '))
        self.Q = int(input('Введіть значення Q: '))
        self.N = self.P * self.Q
        self.message = input('Введіть повідомлення: ')
        self.msg_len = len(self.message)
    
    def __call__(self) -> None:
        r = RabinSystem
        encrypted = [
            r.encrypt(ord(self.message[i]), self.N)
            for i in range(self.msg_len)
        ]
        decrypted = [
            r.decrypt(encrypted[i], self.P, self.Q, self.N)
            for i in range(len(encrypted))
        ]
        print(f'Ваше зашифроване повідомлення: {"".join(str(_) for _ in encrypted)}')
        print(f'Ваше розшифроване повідомлення: {"".join(chr(_) for _ in decrypted)}')
        
if __name__ == '__main__':
    dp = RabinCypher()
    dp()

