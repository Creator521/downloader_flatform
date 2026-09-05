import { Platform } from 'react-native';

export const API_BASE_URL = Platform.OS === 'web'
  ? 'http://localhost:8000'
  : 'https://snapreeldownload.com';

/**
 * Creates FormData from a simple object
 */
export const createFormData = (data: Record<string, string>): FormData => {
  const formData = new FormData();
  Object.keys(data).forEach((key) => {
    formData.append(key, data[key]);
  });
  return formData;
};

/**
 * A generic API request wrapper
 */
export const apiRequest = async <T>(
  endpoint: string,
  method: 'GET' | 'POST',
  body?: Record<string, string>
): Promise<T> => {
  const url = `${API_BASE_URL}${endpoint}`;
  const options: RequestInit = {
    method,
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  };

  if (body) {
    const formBody = [];
    for (const property in body) {
      const encodedKey = encodeURIComponent(property);
      const encodedValue = encodeURIComponent(body[property]);
      formBody.push(encodedKey + "=" + encodedValue);
    }
    options.body = formBody.join("&");
  }

  const response = await fetch(url, options);

  if (!response.ok) {
    let errorDetail = 'API request failed';
    try {
      const errorData = await response.json();
      errorDetail = errorData.detail || errorData.message || errorDetail;
    } catch (e) {
      // Ignored
    }
    throw new Error(errorDetail);
  }

  return response.json();
};
