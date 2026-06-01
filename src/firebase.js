// Firebase configuration and database helpers
// Replace the placeholder values below with your actual Firebase project config.
// To get these values:
//   1. Go to https://console.firebase.google.com
//   2. Create a project (or select an existing one)
//   3. Go to Project Settings > General > Your apps > Web app
//   4. Copy the firebaseConfig object

import { initializeApp } from "firebase/app";
import { getDatabase, ref, set, get, onValue, remove } from "firebase/database";

// ─── Firebase Config ──────────────────────────────────────────────
// REPLACE these with your actual Firebase project credentials
const firebaseConfig = {
  apiKey: "AIzaSyDcLJepnnOpK-LwQX1PhVDQhuIBtxGKgYs",
  authDomain: "pure-advantage-158917.firebaseapp.com",
  databaseURL: "https://pure-advantage-158917-default-rtdb.firebaseio.com",
  projectId: "pure-advantage-158917",
  storageBucket: "pure-advantage-158917.firebasestorage.app",
  messagingSenderId: "807328632872",
  appId: "1:807328632872:web:dbe345d6d340231248e51d",
  measurementId: "G-WHXGRPL7KV",
};

// ─── Initialize ───────────────────────────────────────────────────
const app = initializeApp(firebaseConfig);
const db = getDatabase(app);

// ─── Helper Functions ─────────────────────────────────────────────

/**
 * Write data to a Firebase path.
 * e.g., dbWrite("/users", { alice: {...}, bob: {...} })
 */
export const dbWrite = async (path, data) => {
  try {
    await set(ref(db, path), data);
  } catch (error) {
    console.error(`Firebase write error at ${path}:`, error);
  }
};

/**
 * Read data once from a Firebase path.
 * Returns the data or the fallback value.
 */
export const dbRead = async (path, fallback = null) => {
  try {
    const snapshot = await get(ref(db, path));
    return snapshot.exists() ? snapshot.val() : fallback;
  } catch (error) {
    console.error(`Firebase read error at ${path}:`, error);
    return fallback;
  }
};

/**
 * Subscribe to real-time updates at a Firebase path.
 * Calls `callback(data)` whenever data changes.
 * Returns an unsubscribe function.
 */
export const dbListen = (path, callback, fallback = null, onError = null) => {
  const dbRef = ref(db, path);
  const unsubscribe = onValue(
    dbRef,
    (snapshot) => {
      callback(snapshot.exists() ? snapshot.val() : fallback);
    },
    (error) => {
      console.error(`Firebase listen error at ${path}:`, error);
      if (onError) onError(error);
      callback(fallback);
    }
  );
  return unsubscribe;
};

/**
 * Delete data at a Firebase path.
 */
export const dbRemove = async (path) => {
  try {
    await remove(ref(db, path));
  } catch (error) {
    console.error(`Firebase remove error at ${path}:`, error);
  }
};

export const dbUrl = firebaseConfig.databaseURL;

export { db };
