def load_secrets(filename):
    secrets = []
    with open(filename, 'r') as file:
        for line in file:
            if not line.strip():
                continue
            secrets.append(int(line.strip()))
    return secrets




def next_secret(secret):
    to_mix = secret << 6
    mixed = to_mix ^ secret
    pruned = mixed - ((mixed >> 24) << 24)
    
    s2 = pruned >> 5
    s2_modulo = pruned - (s2 << 5)
    s2_mixed = s2 ^ pruned
    s2_pruned = s2_mixed - ((s2_mixed >> 24) << 24)
    
    s3 = s2_pruned << 11
    s3_mixed = s3 ^ s2_pruned
    s3_pruned = s3_mixed - ((s3_mixed >> 24) << 24)
    return s3_pruned


def roll_secret(secret, n=10): 
    for _ in range(n):
        secret = next_secret(secret)
        print(secret)
    return secret

def roll_secret_p2(secret, n=10): 
    ones = [secret % 10]
    price_changes = [secret % 10]
    price_change_sets = [tuple()]
    # print(secret, ': ', ones[-1], price_changes[-1])
    for _ in range(n):
        secret = next_secret(secret)
        ones.append(secret % 10)
        price_changes.append(ones[-1] - ones[-2])
        if len(ones) > 3:
            price_change_sets.append(tuple(price_changes[-4:]))
            # print(secret, ': ', ones[-1], price_changes[-4:])
        else:
            price_change_sets.append(tuple())
            # print(secret, ': ', ones[-1], price_changes[-1])
    return secret, ones, price_change_sets

def find_magic_price_change_set(prices, price_change_sets):
    i = 0
    magic_price_change_set = {}
    for buyer in range(len(price_change_sets)):
        for i in range(3,len(price_change_sets[buyer])):
            if price_change_sets[buyer][i] not in magic_price_change_set:
                magic_price_change_set[price_change_sets[buyer][i]] = [(buyer,i,prices[buyer][i])]
            else:
                # if (buyer,prices[buyer][i]) not in [(mp[0],mp[2]) for mp in magic_price_change_set[price_change_sets[buyer][i]]]:
                if buyer not in [mp[0] for mp in magic_price_change_set[price_change_sets[buyer][i]]]:
                    magic_price_change_set[price_change_sets[buyer][i]].append((buyer,i,prices[buyer][i]))
    # [print(mpcs, sum(mp[2] for mp in magic_price_change_set[mpcs]),  magic_price_change_set[mpcs]) for mpcs in magic_price_change_set]
    sum_prices = [sum(mp[2] for mp in magic_price_change_set[mpcs]) for mpcs in magic_price_change_set]
    # [print(s) for s in sum_prices]
    print(max(sum_prices))



def guess_secrets(secrets):
    
    # roll_secret_p2(3, 2000)
    # return
    buyer_secrets = []
    buyer_prices = []
    buyer_price_change_sets = []
    for secret in secrets:
        n, ones, price_changes = roll_secret_p2(secret,2000)
        # print(secret, ': ', n)
        buyer_secrets.append(n)
        buyer_prices.append(ones)
        buyer_price_change_sets.append(price_changes)
    find_magic_price_change_set(buyer_prices, buyer_price_change_sets)
    print(sum(buyer_secrets))



if __name__ == "__main__":
    initial_secrets = load_secrets('day22_pseudo.txt')
    # initial_secrets = load_secrets('day22_pseudo_sample.txt')
    guess_secrets(initial_secrets)
