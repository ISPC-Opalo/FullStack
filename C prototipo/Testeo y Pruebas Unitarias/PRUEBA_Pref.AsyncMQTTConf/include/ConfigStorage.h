#pragma once
#include <Preferences.h>

class ConfigStorage {
public:
  ConfigStorage(const char* ns = "config") : _ns(ns), _isOpen(false) {}

  bool begin(bool readOnly = false) {
    if (_isOpen) return true;
    _isOpen = _prefs.begin(_ns, readOnly);
    return _isOpen;
  }

  int getInt(const char* key, int def)       { return _prefs.getInt(key, def); }
  unsigned long getULong(const char* key, unsigned long def) { return _prefs.getULong(key, def); }
  bool getBool(const char* key, bool def)     { return _prefs.getBool(key, def); }
  String getString(const char* key, const char* def) {
    return _prefs.getString(key, def);
  }

  void putInt   (const char* key, int v)    { _prefs.putInt(key, v); }
  void putULong (const char* key, unsigned long v) { _prefs.putULong(key, v); }
  void putBool  (const char* key, bool v)   { _prefs.putBool(key, v); }
  void putString(const char* key, const char* v) { _prefs.putString(key, v); }

  void end() {
    if (_isOpen) {
      _prefs.end();
      _isOpen = false;
    }
  }

private:
  Preferences _prefs;
  const char* _ns;
  bool        _isOpen;
};
