import './globals.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import MyNavbar from './components/MyNavbar';

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <MyNavbar />
        {children}
      </body>
    </html>
  );
}
