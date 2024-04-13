{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = inputs@{ flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      systems = [ "x86_64-linux" "aarch64-linux" ];
      perSystem = { pkgs, ... }: {
        devShells.default = pkgs.mkShell {
          name = "projet-session";
          packages = with pkgs; [
            postgresql_12
            redis
          ];
          buildInputs = with pkgs; [
            libpqxx
          ];
        };
      };
    };
}
