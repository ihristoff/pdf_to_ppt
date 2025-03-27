'use client';

import { useState, useCallback } from 'react';
import { ArrowUpTrayIcon, DocumentIcon, ArrowDownTrayIcon } from '@heroicons/react/24/outline';
import axios from 'axios';

export default function Home() {
  const [file, setFile] = useState(null);
  const [converting, setConverting] = useState(false);
  const [error, setError] = useState(null);
  const [downloadUrl, setDownloadUrl] = useState(null);
  const [isDragging, setIsDragging] = useState(false);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    handleFile(selectedFile);
  };

  const handleFile = (selectedFile) => {
    if (selectedFile?.type === 'application/pdf') {
      setFile(selectedFile);
      setError(null);
      setDownloadUrl(null);
    } else {
      setError('Please select a valid PDF file');
      setFile(null);
    }
  };

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    setIsDragging(false);
    const droppedFile = e.dataTransfer.files[0];
    handleFile(droppedFile);
  }, []);

  const handleDragOver = useCallback((e) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;

    setConverting(true);
    setError(null);
    setDownloadUrl(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('/api/convert', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        responseType: 'blob',
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      setDownloadUrl(url);
    } catch (err) {
      setError('Error converting file. Please try again.');
      console.error('Conversion error:', err);
    } finally {
      setConverting(false);
    }
  };

  return (
    <div className="gradient-bg">
      <main className="container-custom relative z-10">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 sm:text-5xl mb-4 bg-clip-text text-transparent bg-gradient-to-r from-primary to-primary-dark">
            PDF to PowerPoint Converter
          </h1>
          <p className="text-lg text-gray-600">
            Transform your PDF files into editable PowerPoint presentations
          </p>
        </div>

        <div className="card">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div
              className={`upload-area ${isDragging ? 'dragging' : ''}`}
              onDrop={handleDrop}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onClick={() => document.getElementById('file-input').click()}
            >
              <input
                id="file-input"
                type="file"
                className="hidden"
                accept=".pdf"
                onChange={handleFileChange}
              />
              
              <div className="flex flex-col items-center gap-4">
                {file ? (
                  <>
                    <DocumentIcon className="h-16 w-16 text-primary" />
                    <div className="text-center">
                      <p className="text-sm font-medium text-gray-900">{file.name}</p>
                      <p className="text-xs text-gray-500 mt-1">
                        {(file.size / (1024 * 1024)).toFixed(2)} MB
                      </p>
                    </div>
                  </>
                ) : (
                  <>
                    <ArrowUpTrayIcon className="h-16 w-16 text-gray-400" />
                    <div className="text-center">
                      <p className="text-sm font-medium text-gray-900">
                        Drop your PDF here or click to browse
                      </p>
                      <p className="text-xs text-gray-500 mt-1">
                        PDF files up to 10MB
                      </p>
                    </div>
                  </>
                )}
              </div>
            </div>

            {error && (
              <div className="text-center">
                <p className="text-sm text-red-600">{error}</p>
              </div>
            )}

            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button
                type="submit"
                disabled={!file || converting}
                className="btn-primary"
              >
                {converting ? (
                  <>
                    <svg
                      className="animate-spin h-5 w-5"
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                    >
                      <circle
                        className="opacity-25"
                        cx="12"
                        cy="12"
                        r="10"
                        stroke="currentColor"
                        strokeWidth="4"
                      ></circle>
                      <path
                        className="opacity-75"
                        fill="currentColor"
                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                      ></path>
                    </svg>
                    Converting...
                  </>
                ) : (
                  <>
                    Convert to PowerPoint
                  </>
                )}
              </button>

              {downloadUrl && (
                <a
                  href={downloadUrl}
                  download="converted.pptx"
                  className="btn-secondary"
                >
                  <ArrowDownTrayIcon className="h-5 w-5" />
                  Download PowerPoint
                </a>
              )}
            </div>
          </form>
        </div>
      </main>
    </div>
  );
} 