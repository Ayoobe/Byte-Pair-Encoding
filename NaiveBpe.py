from utils import stats, merge


class NaiveBpe:

    def __init__(self):
        self.vocab = None
        self.merges = None

    def train(self, corpus, vocab_size ):
        assert vocab_size >= 256
        num_merges = vocab_size - 255

        merges = {}  # (int, int) -> int
        vocab = {idx: bytes([idx]) for idx in range(256)}  # int -> bytes

        tokens = list(corpus.encode("utf-8"))
        for i in range(vocab_size):
            stat = stats(tokens)
            if not stat:
                break
            pair = max(stat, key=stat.get)
            idx = 255 + i
            tokens = merge(tokens, pair, idx)
            merges[pair] = idx
            vocab[idx] = vocab[pair[0]] + vocab[pair[1]]


        self.merges = merges
        self.vocab = vocab

    def decode(self, tokens):
        my_bytes = b"".join(self.vocab[i] for i in tokens)
        text = my_bytes.decode("utf-8", errors="replace")
        return text

    def encode(self, text):
        tokens = list(text.encode("utf-8"))
        while len(tokens) >= 2:
            stat = stats(tokens)
            pair = min(stat, key=lambda p: self.merges.get(p, float("inf")))

            if pair not in self.merges:
                break  # nothing else can be merged anymore
            # otherwise let's merge the best pair (lowest merge index)
            idx = self.merges[pair]
            tokens = merge(tokens, pair, idx)
        return tokens


# Test Code for NaiveBpe Class

# Sample corpus (text) to train on
corpus = "hello hello hello"

# Initialize NaiveBpe model
bpe_model = NaiveBpe()

# Train the model with a desired vocabulary size
vocab_size = 400  # Set a higher vocab size if you want more merges
bpe_model.train(corpus, vocab_size )

# Encode a new text
text_to_encode = "hello hello"
encoded_tokens = bpe_model.encode(text_to_encode)
print(f"Encoded tokens: {encoded_tokens}")
print(bpe_model.merges)
print(bpe_model.vocab)

# Decode the tokens back to text
decoded_text = bpe_model.decode(encoded_tokens)
print(f"Decoded text: {decoded_text}")

