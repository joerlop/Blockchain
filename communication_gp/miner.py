import hashlib
import requests
import json

import sys


# TODO: Implement functionality to search for a proof
def proof_of_work(block):

    block_string = json.dumps(block, sort_keys=True).encode()

    proof = 0
    while valid_proof(block_string, proof) is False:
        proof += 1

    return proof


def valid_proof(block_string, proof):

    guess = f"{block_string}{proof}".encode()
    guess_hash = hashlib.sha256(guess).hexdigest()

    # TODO: Change back to six zeroes
    return guess_hash[:5] == "00000"


if __name__ == "__main__":
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    coins_mined = 0
    proof = 0
    # Run forever until interrupted
    while True:
        # TODO: Get the last proof from the server and look for a new one
        response = requests.get("http://localhost:5000/last_block").json()
        # TODO: When found, POST it to the server {"proof": new_proof}
        # TODO: We're going to have to research how to do a POST in Python
        # HINT: Research `requests` and remember we're sending our data as JSON
        # TODO: If the server responds with 'New Block Forged'
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.
        last_block = response["last_block"]

        new_proof = proof_of_work(last_block)

        json_proof_response = requests.post(
            "http://localhost:5000/mine", json={"proof": f"{new_proof}"}
        ).json()

        if json_proof_response["message"] == "failure":
            print(json_proof_response["message"])

        else:
            coins_mined += 1
            print(json_proof_response["message"])
            print(f"Coins mined: {coins_mined}")

