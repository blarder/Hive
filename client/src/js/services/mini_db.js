/**
 * Created by brettlarder on 17/02/2015.
 */
angular.module('MiniDB', [])
    .factory('MiniDB', [function() {

        var socket = null;
        var updateCallback = null;

        var db = {};
        var tableArrays = {};
        var max = 50;

        var aliasMap = { // Attribute names that are foreign/many-to-many keys to other tables
            staff_member: 'user',
            channels: 'channel',
            subscriptions: 'channel'
        };

        var createTableIfAbsent = function(table) {
            if (aliasMap[table]) {
                table = aliasMap[table]
            }

            if (!db[table]) {
                db[table] = {};
                tableArrays[table] = [];
            }
        };

        var getDBTable = function(table) {
            createTableIfAbsent(table);
            return db[table]
        };

        var getTableArray = function(table) {
            createTableIfAbsent(table);
            return tableArrays[table]
        };

        var additionalProcessingMap = { // function applied in create/update function when tableName is matched
            // returns a bool indicating whether a table should still be created for this object type
            event_log: function(log) {db.event[log.event_id].log.push(log); return false},
            chat: function() {return false}
        };

        var deleteItem = function(tableName, item) {
            for (var key in db[tableName][item.id]) {
                if (db[tableName][item.id].hasOwnProperty(key)) {
                    delete db[tableName][item.id][key]
                }
            }
        };

        var createOrUpdate = function(tableName, item) {

            if (angular.isArray(item)) {
                for (var i = 0; i < item.length; ++i) {
                    item[i] = createOrUpdate(tableName, item[i])
                }
                return item
            } else {
                for (var att in item) {
                    if (item.hasOwnProperty(att)) {
                        if (angular.isObject(item[att]) && !angular.isDate(item[att])) {
                            item[att] = createOrUpdate(att, item[att])
                        }
                    }
                }
            }

            if (additionalProcessingMap[tableName] && !additionalProcessingMap[tableName](item)) {
                return item
            }

            if (aliasMap[tableName]) {
                tableName = aliasMap[tableName]
            }

            if (!db[tableName]) {
                db[tableName] = {};
                tableArrays[tableName] = []
            }

            if (db[tableName][item.id]) {
                return angular.extend(db[tableName][item.id], item)
            }

            db[tableName][item.id] = item;
            tableArrays[tableName].push(item);
            return item

        };

        var connect = function(sock) {
            socket = sock;
            socket.on('message', function(message) {
                var messageObj = angular.fromJson(message);
                var deletionIndex = messageObj.message_type.indexOf('_deletion');
                if (deletionIndex != -1) {
                    return deleteItem(messageObj.message_type.substring(0, deletionIndex), messageObj)
                }
                var updateData = createOrUpdate(messageObj.message_type, messageObj);
                if (updateCallback) {
                    updateCallback(updateData)
                }
            });
        };

        return {
            update: createOrUpdate,
            setUpdateCallback: function(callback) {updateCallback = callback},
            connectSocket: connect,
            get: function() {return db},
            getTable: getDBTable,
            getArray: getTableArray
        }

    }]);