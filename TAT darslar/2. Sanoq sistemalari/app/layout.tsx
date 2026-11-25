import type {Metadata, Viewport} from 'next';
import './globals.css';

const TITLE = 'Tibbiyotda Axborot Texnologiyalari — Interaktiv qo‘llanma';
const DESCRIPTION =
  'Shahrisabz Tibbiyot Texnikumi, hamshiralik ishi yo‘nalishi uchun "Tibbiyotda axborot texnologiyalari" fanidan interaktiv elektron qo‘llanma, amaliy simulyator va test tizimi.';

export const metadata: Metadata = {
  title: {default: TITLE, template: '%s — Tibbiyotda AT'},
  description: DESCRIPTION,
  applicationName: 'Tibbiyotda AT',
  openGraph: {title: TITLE, description: DESCRIPTION, type: 'website'},
  twitter: {card: 'summary_large_image', title: TITLE, description: DESCRIPTION},
};

export const viewport: Viewport = {
  themeColor: '#060b15',
};

/**
 * Sayt doim tungi (dark) rejimda ishlaydi - yorug' yoki tizim rejimiga
 * almashtirish imkoni ataylab olib tashlangan. Shunga qaramay bu skript
 * birinchi chizishdan oldin ishlaydi, chunki eski qurilmalarda saqlanib
 * qolgan "light" tanlovi bo'lsa ham, sahifa bir zum yorug' ko'rinib
 * ketmasligi kerak.
 */
const THEME_BOOT = `(function(){try{localStorage.removeItem('tat-theme')}catch(e){}document.documentElement.dataset.theme='dark';document.documentElement.dataset.themeMode='dark'})()`;

export default function RootLayout({children}: {children: React.ReactNode}) {
  return (
    <html lang="uz" suppressHydrationWarning>
      <head>
        <script dangerouslySetInnerHTML={{__html: THEME_BOOT}} />
      </head>
      <body suppressHydrationWarning>{children}</body>
    </html>
  );
}
