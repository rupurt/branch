{
  description = "Development environment for Branch. A streaming toolkit with bottomless storage";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    flake-utils,
    nixpkgs,
    ...
  }: let
    systems = ["x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin"];
    outputs = flake-utils.lib.eachSystem systems (system: let
      pkgs = import nixpkgs {
        inherit system;
        overlays = [];
      };
    in {
      # packages exported by the flake
      packages = {};

      # nix run
      apps = {};

      # nix fmt
      formatter = pkgs.alejandra;

      # nix develop -c $SHELL
      # devShells.default = pkgs.mkShellNoCC {
      devShells.default = pkgs.mkShell {
        name = "default dev shell";
        # LD_LIBRARY_PATH =
        #   if (pkgs.stdenv.isLinux)
        #   then
        #     pkgs.lib.makeLibraryPath [
        #       pkgs.stdenv.cc.cc.lib
        #       pkgs.zlib
        #       pkgs.openssl
        #     ]
        #   else [];
        packages = with pkgs;
          [
            modd
            (python311.withPackages (ps:
              with ps; [
                pip
                virtualenv
                ipython
              ]))
            python311Packages.venvShellHook
          ]
          ++ pkgs.lib.optionals (pkgs.stdenv.isLinux) [
            cosmocc
            cosmopolitan
          ];
        venvDir = ".venv";
      };
    });
  in
    outputs;
}
