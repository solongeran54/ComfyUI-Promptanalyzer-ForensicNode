// =====================================================
// NOTE / LICENSE
// =====================================================
//
// Script & Function by: https://github.com/solongeran54
// Built in 2025
//
// MIT License
//(You are free to use, modify, and integrate this node in commercial and non-commercial
// projects.)
//   
// Please respect the author’s work and time
//
// All Rights Reserved © 2025
//
// You are welcome to share and contribute to the Open Source community.
// 
// This Node is developed in the great EU (Germany2025)
// =====================================================

import { app } from "../../../scripts/app.js";

app.registerExtension({
    name: "KI_GlassLensHUD",

    nodeCreated(node) {
        const activeClasses = new Set(["TokenCheckpointAnalytics"]);
        if (!activeClasses.has(node.comfyClass)) return;

        node._pulse = 0;

        node._hudLoop = () => {
            node._pulse += 0.02; // sehr sanft
            node.setDirtyCanvas(true, true);
            node._hudAnimationFrame = requestAnimationFrame(node._hudLoop);
        };
        if (!node._hudAnimationFrame) node._hudLoop();

        node.onDrawBackground = function(ctx) {
            const w = node.size[0];
            const h = node.size[1];
            const centerX = w / 2;
            const centerY = h / 2;
            const lensRadius = Math.min(w, h) / 6;

            ctx.save();
            ctx.clearRect(0, 0, w, h);

            // --- Schwarzer Hintergrund ---
            ctx.fillStyle = "rgba(0,0,0,0.90)";
            ctx.fillRect(0, 0, w, h);

            // --- Glaslinse ---
            const gradient = ctx.createRadialGradient(
                centerX - lensRadius * 0.2 * Math.sin(node._pulse), 
                centerY - lensRadius * 0.2 * Math.cos(node._pulse), 
                lensRadius * 0.05, 
                centerX, 
                centerY, 
                lensRadius
            );
            gradient.addColorStop(0, "rgba(255,100,100,1)");
            gradient.addColorStop(0.3, "rgba(200,50,50,0.8)");
            gradient.addColorStop(0.7, "rgba(150,0,0,0.5)");
            gradient.addColorStop(1, "rgba(80,0,0,0.2)");

            ctx.fillStyle = gradient;
            ctx.beginPath();
            ctx.arc(centerX, centerY, lensRadius, 0, 2 * Math.PI);
            ctx.fill();

            // --- Silberner Ring ---
            ctx.strokeStyle = "rgba(200,200,200,0.8)";
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.arc(centerX, centerY, lensRadius, 0, 2 * Math.PI);
            ctx.stroke();

            ctx.restore();
        };

        node.onDelete = () => {
            if (node._hudAnimationFrame) {
                cancelAnimationFrame(node._hudAnimationFrame);
                node._hudAnimationFrame = null;
            }
        };

        node.setDirtyCanvas(true, true);
    }
});






























