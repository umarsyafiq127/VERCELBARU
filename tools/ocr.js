const express = require("express");
const multer = require("multer");
const Tesseract = require("tesseract.js");
const cors = require("cors");

const app = express();
app.use(cors());

const upload = multer({ storage: multer.memoryStorage() });

app.post("/ocr", upload.single("image"), (req, res) => {
    if (!req.file) return res.status(400).json({ error: "File tidak ditemukan." });

    Tesseract.recognize(req.file.buffer, "eng", {
        logger: (m) => console.log(m),
    }).then(({ data: { text } }) => {
        res.json({ text: text.replace(/\n/g, "<br>") || "Teks tidak ditemukan atau tidak terbaca." });
    }).catch(err => res.status(500).json({ error: err.toString() }));
});

const PORT = 5001;
app.listen(PORT, () => {
    console.log(`OCR Server berjalan di http://localhost:${PORT}`);
});
