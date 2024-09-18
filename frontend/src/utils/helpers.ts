import CryptoJS from "crypto-js";

export const encryptToken = (token: string) => {
  const encryptionKey = process.env.REACT_APP_ENCRYPTION_KEY as string;
  const encryptedToken = CryptoJS.AES.encrypt(token, encryptionKey).toString();
  return encryptedToken;
};

export const decryptToken = (encryptedToken: string) => {
  const encryptionKey = process.env.REACT_APP_ENCRYPTION_KEY as string;
  const decryptedToken = CryptoJS.AES.decrypt(
    encryptedToken,
    encryptionKey
  ).toString(CryptoJS.enc.Utf8);
  return decryptedToken;
};
