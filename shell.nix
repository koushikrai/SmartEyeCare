{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    # Python 3.11 with required packages
    (python311.withPackages (ps: with ps; [
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
    ]))
    
    # Node.js for frontend
    nodejs_20
    npm
  ];

  shellHook = ''
    echo "SmartEyeCare Development Environment"
    echo "Python version: $(python --version)"
    echo "Node version: $(node --version)"
    echo ""
    echo "Installing additional Python dependencies from requirements.txt..."
    pip install -r backend/requirements.txt || true
    echo ""
    echo "Environment ready!"
    echo "To start the backend: python backend/app.py"
    echo "To start the frontend: cd frontend && npm run dev"
  '';
}

