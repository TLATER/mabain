{ pkgs ? import <nixpkgs> { } }:

let
  python = pkgs.python3.withPackages (ppkgs:
    with ppkgs; [
      python-lsp-server
      python-lsp-black
      pyls-isort
      pylsp-mypy

      rope
      pyflakes
      mccabe
      pycodestyle
      pydocstyle
    ]);

in pkgs.mkShell {
  nativeBuildInputs = with pkgs; [ bazelisk buildifier python ];
}
