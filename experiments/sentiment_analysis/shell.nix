with import <nixpkgs> {};
stdenv.mkDerivation rec {
  name = "sentiment-hackyhour";
  env = buildEnv { name = name; paths = buildInputs; };
  buildInputs = [
    python3
    python3Packages.tweepy
    python3Packages.nltk
  ];
}
