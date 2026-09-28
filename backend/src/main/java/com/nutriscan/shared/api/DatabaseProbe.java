package com.nutriscan.shared.api;

import java.sql.Connection;
import java.sql.SQLException;
import java.time.Duration;
import javax.sql.DataSource;
import org.springframework.beans.factory.ObjectProvider;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.util.Assert;

/** Reports UP only after a connection was actually validated; anything short of that is not UP (S8, K03). */
@Component
class DatabaseProbe {

    private final ObjectProvider<DataSource> dataSource;
    private final int timeoutSeconds;

    DatabaseProbe(ObjectProvider<DataSource> dataSource,
            @Value("${nutriscan.system.database-check-timeout}") Duration timeout) {
        // Connection.isValid takes whole seconds and reads 0 as "wait forever".
        Assert.isTrue(timeout.toSeconds() >= 1, "nutriscan.system.database-check-timeout must be at least 1s");
        this.dataSource = dataSource;
        this.timeoutSeconds = Math.toIntExact(timeout.toSeconds());
    }

    DatabaseStatus check() {
        DataSource configured = dataSource.getIfAvailable();
        if (configured == null) {
            return DatabaseStatus.NOT_CONFIGURED;
        }
        try (Connection connection = configured.getConnection()) {
            return connection.isValid(timeoutSeconds) ? DatabaseStatus.UP : DatabaseStatus.DOWN;
        } catch (SQLException e) {
            // Not logged: the message may carry the JDBC URL; the status is the whole answer.
            return DatabaseStatus.DOWN;
        }
    }
}
