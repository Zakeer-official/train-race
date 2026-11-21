import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#080c14",
        surface: "#0d1527",
        "surface-card": "#131e36",
        "surface-border": "#1e2f52",
        rail: {
          cyan: "#00f0ff",
          blue: "#2563eb",
          leader: "#10b981",
          amber: "#f59e0b",
          red: "#ef4444",
        },
      },
    },
  },
  plugins: [],
};
export default config;
