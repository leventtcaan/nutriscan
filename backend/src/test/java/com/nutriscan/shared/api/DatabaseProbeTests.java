package com.nutriscan.shared.api;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatIllegalArgumentException;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import java.sql.Connection;
import java.sql.SQLException;
import java.time.Duration;
import javax.sql.DataSource;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.ObjectProvider;
import org.springframework.beans.factory.support.StaticListableBeanFactory;

/** The ping never reports a database as UP unless a connection was actually validated (S8, K03). */
class DatabaseProbeTests {

    private static final Duration TIMEOUT = Duration.ofSeconds(1);

    @Test
    void notConfiguredWithoutDataSource() {
        assertThat(new DatabaseProbe(provider(null), TIMEOUT).check()).isEqualTo(DatabaseStatus.NOT_CONFIGURED);
    }

    @Test
    void upWhenConnectionIsValid() throws SQLException {
        assertThat(new DatabaseProbe(provider(dataSourceWithValidConnection(true)), TIMEOUT).check())
                .isEqualTo(DatabaseStatus.UP);
    }

    @Test
    void downWhenConnectionIsNotValid() throws SQLException {
        assertThat(new DatabaseProbe(provider(dataSourceWithValidConnection(false)), TIMEOUT).check())
                .isEqualTo(DatabaseStatus.DOWN);
    }

    @Test
    void downWhenConnectionCannotBeObtained() throws SQLException {
        DataSource dataSource = mock(DataSource.class);
        when(dataSource.getConnection()).thenThrow(new SQLException("connection refused"));

        assertThat(new DatabaseProbe(provider(dataSource), TIMEOUT).check()).isEqualTo(DatabaseStatus.DOWN);
    }

    @Test
    void rejectsTimeoutShorterThanOneSecond() {
        // Connection.isValid takes whole seconds and treats 0 as "no timeout".
        assertThatIllegalArgumentException()
                .isThrownBy(() -> new DatabaseProbe(provider(null), Duration.ofMillis(500)));
    }

    private static DataSource dataSourceWithValidConnection(boolean valid) throws SQLException {
        Connection connection = mock(Connection.class);
        when(connection.isValid((int) TIMEOUT.toSeconds())).thenReturn(valid);
        DataSource dataSource = mock(DataSource.class);
        when(dataSource.getConnection()).thenReturn(connection);
        return dataSource;
    }

    private static ObjectProvider<DataSource> provider(DataSource dataSource) {
        StaticListableBeanFactory beanFactory = new StaticListableBeanFactory();
        if (dataSource != null) {
            beanFactory.addBean("dataSource", dataSource);
        }
        return beanFactory.getBeanProvider(DataSource.class);
    }
}
