{
  description = "SmartEyeCare Development Environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
        };

        pythonEnv = pkgs.python311.withPackages (ps: with ps; [
          flask
          flask-cors
          opencv4
          tensorflow
          scikit-learn
          numpy
          pandas
          pymongo
          bcrypt
          scipy
          python-dotenv
          mediapipe
          pillow
        ]);

      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            pythonEnv
            nodejs_20
            npm
          ];

          shellHook = ''
            echo "SmartEyeCare Development Environment"
            echo "Python version: $(python --version)"
            echo "Node version: $(node --version)"
            echo ""
            echo "Installing Python dependencies..."
            pip install -r backend/requirements.txt
            echo ""
            echo "To start the backend: python backend/app.py"
            echo "To start the frontend: cd frontend && npm run dev"
          '';
        };
      }
    );
}

