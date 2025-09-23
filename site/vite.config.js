import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";
import fs from "fs"

// https://vitejs.dev/config/
export default ({ mode }) => {
    process.env = { ...process.env, ...loadEnv(mode, process.cwd()) };

    return defineConfig({
        plugins: [react()],
        base: "./",
        server: {
            host: true,
            port: 8080,
            https: {
              key: fs.readFileSync(process.env.VITE_PRIVKEY),
              cert: fs.readFileSync(process.env.VITE_CERT),
            },
            proxy: {
                "/api": {
                    target: "http://localhost:5000",
                    changeOrigin: true,
                    secure: false,
                    configure: (proxy) => {
                        proxy.on("proxyReq", (proxyReq) => {
                        // override the default UA with something non-standard
                        proxyReq.setHeader(
                            "User-Agent",
                            "ngrok-agent"
                        );
                        });
                    },
                },
            }
        },
    });
};
