import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [uploadResult, setUploadResult] = useState(null);

  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const [summary, setSummary] = useState("");
  const [sources, setSources] = useState([]);

  const [uploadLoading, setUploadLoading] = useState(false);
  const [askLoading, setAskLoading] = useState(false);
  const [summaryLoading, setSummaryLoading] = useState(false);

  const API_URL = "http://127.0.0.1:8003";


  // ==================================================
  // UPLOAD PDF
  // ==================================================

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a PDF file.");
      return;
    }

    try {
      setUploadLoading(true);

      const formData = new FormData();
      formData.append("file", file);

      const response = await axios.post(
        `${API_URL}/upload`,
        formData
      );

      setUploadResult(response.data);

      setAnswer("");
      setSummary("");
      setSources([]);

    } catch (error) {
      console.error(error);

      const message =
        error.response?.data?.message ||
        error.response?.data?.detail ||
        "PDF upload failed.";

      alert(message);

    } finally {
      setUploadLoading(false);
    }
  };


  // ==================================================
  // ASK AI
  // ==================================================

  const askQuestion = async () => {
    if (!question.trim()) {
      alert("Please enter a question.");
      return;
    }

    if (!uploadResult) {
      alert("Please upload a PDF first.");
      return;
    }

    try {
      setAskLoading(true);
      setAnswer("");
      setSources([]);

      const response = await axios.get(
        `${API_URL}/ask`,
        {
          params: {
            query: question,
            top_k: 3
          },
          timeout: 15000
        }
      );

      setAnswer(response.data.answer);

      setSources(
        response.data.sources || []
      );

    } catch (error) {
      console.error(error);

      if (error.code === "ECONNABORTED") {
        setAnswer(
          "The AI request took too long. Your Gemini free-tier quota may currently be unavailable. Please try again later."
        );
      } else {
        const message =
          error.response?.data?.message ||
          error.response?.data?.detail ||
          "Unable to get AI answer.";

        setAnswer(message);
      }

    } finally {
      setAskLoading(false);
    }
  };


  // ==================================================
  // SUMMARIZE DOCUMENT
  // ==================================================

  const summarizeDocument = async () => {
    if (!uploadResult) {
      alert("Please upload a PDF first.");
      return;
    }

    try {
      setSummaryLoading(true);
      setSummary("");
      setSources([]);

      const response = await axios.get(
        `${API_URL}/summarize`,
        {
          params: {
            document_name: uploadResult.filename,
            top_k: 10
          },
          timeout: 15000
        }
      );

      setSummary(response.data.summary);

      setSources(
        response.data.sources || []
      );

    } catch (error) {
      console.error(error);

      if (error.code === "ECONNABORTED") {
        setSummary(
          "The summary request took too long. Your Gemini free-tier quota may currently be unavailable. Please try again later."
        );
      } else {
        const message =
          error.response?.data?.message ||
          error.response?.data?.detail ||
          "Unable to summarize document.";

        setSummary(message);
      }

    } finally {
      setSummaryLoading(false);
    }
  };


  // ==================================================
  // UI
  // ==================================================

  return (
    <div className="app">

      {/* HEADER */}

      <header className="header">

        <div>

          <h1>
            DocuPilot AI
          </h1>

          <p>
            AI-Powered Document Intelligence Assistant
          </p>

        </div>

      </header>


      <main className="container">


        {/* ========================================= */}
        {/* UPLOAD DOCUMENT */}
        {/* ========================================= */}

        <section className="card">

          <h2>
            Upload Document
          </h2>

          <p className="description">
            Upload a PDF and let DocuPilot AI understand your document.
          </p>


          <input
            type="file"
            accept=".pdf"
            onChange={(e) => {
              setFile(e.target.files[0]);
            }}
          />


          <button
            onClick={handleUpload}
            disabled={uploadLoading}
          >

            {uploadLoading
              ? "Processing..."
              : "Upload PDF"}

          </button>


          {uploadResult && (

            <div className="success-box">

              <h3>
                Document Processed ✓
              </h3>


              <p>
                <strong>File:</strong>{" "}
                {uploadResult.filename}
              </p>


              <p>
                <strong>Pages:</strong>{" "}
                {uploadResult.total_pages}
              </p>


              <p>
                <strong>Characters:</strong>{" "}
                {uploadResult.total_characters}
              </p>


              <p>
                <strong>Chunks:</strong>{" "}
                {uploadResult.total_chunks}
              </p>

            </div>

          )}

        </section>


        {/* ========================================= */}
        {/* ASK DOCUMENT */}
        {/* ========================================= */}

        <section className="card">

          <h2>
            Ask Your Document
          </h2>

          <p className="description">
            Ask questions and get answers based on your uploaded PDF.
          </p>


          <div className="question-row">

            <input
              type="text"
              placeholder="Example: Where did the person work?"
              value={question}
              onChange={(e) => {
                setQuestion(e.target.value);
              }}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  askQuestion();
                }
              }}
            />


            <button
              onClick={askQuestion}
              disabled={
                askLoading ||
                !uploadResult
              }
            >

              {askLoading
                ? "Thinking..."
                : "Ask AI"}

            </button>

          </div>


          {answer && (

            <div className="answer-box">

              <h3>
                AI Answer
              </h3>

              <p>
                {answer}
              </p>

            </div>

          )}

        </section>


        {/* ========================================= */}
        {/* DOCUMENT SUMMARY */}
        {/* ========================================= */}

        <section className="card">

          <h2>
            Document Summary
          </h2>

          <p className="description">
            Generate an AI-powered summary of your uploaded document.
          </p>


          <button
            onClick={summarizeDocument}
            disabled={
              summaryLoading ||
              !uploadResult
            }
          >

            {summaryLoading
              ? "Generating..."
              : "Summarize Document"}

          </button>


          {summary && (

            <div className="summary-box">

              <h3>
                AI Summary
              </h3>

              <div className="summary-text">
                {summary}
              </div>

            </div>

          )}

        </section>


        {/* ========================================= */}
        {/* SOURCES */}
        {/* ========================================= */}

        {sources.length > 0 && (

          <section className="card">

            <h2>
              Sources
            </h2>


            <div className="sources">

              {sources.map(
                (source, index) => (

                  <div
                    className="source-item"
                    key={index}
                  >

                    <strong>
                      Source {index + 1}
                    </strong>


                    <p>
                      Document:{" "}
                      {source.document}
                    </p>


                    <p>
                      Page:{" "}
                      {source.page}
                    </p>

                  </div>

                )
              )}

            </div>

          </section>

        )}

      </main>

    </div>
  );
}

export default App;