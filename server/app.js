const express = require("express");
const fs = require("fs");
const { ParquetWriter, ParquetSchema } = require("parquetjs");
const path = require("path");

const app = express();
const PORT = 3000;

// Function to generate a Parquet file
async function generateParquetFile(filePath) {
    const schema = new ParquetSchema({
        name: { type: "UTF8" },
        age: { type: "INT32" },
        city: { type: "UTF8" },
    });
    const writer = await ParquetWriter.openFile(schema, filePath);
    await writer.appendRow({ name: "Alice", age: 25, city: "New York" });
    await writer.appendRow({ name: "Bob", age: 30, city: "San Francisco" });
    await writer.appendRow({ name: "Charlie", age: 35, city: "Seattle" });
    await writer.close();
}

// Endpoint to send the Parquet file
app.get("/download", async (req, res) => {
    const dirPath = path.join(__dirname, 'data');
    const filePath = path.join(dirPath, 'example.parquet');

    try {
        // Create the directory if it doesn't exist
        if (!fs.existsSync(dirPath)) {
            fs.mkdirSync(dirPath);
        }

        // Generate the Parquet file
        await generateParquetFile(filePath);

        // Send the Parquet file
        res.download(filePath);
    } catch (error) {
        console.error("Error generating or sending Parquet file:", error);
        res.status(500).send("Error generating or sending Parquet file");
    }
});

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});