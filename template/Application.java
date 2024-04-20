package {{pkgName}};

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.properties.EnableConfigurationProperties;

/**
 * @author xxp
 * @since 2023/10/10
 */
@MapperScan("{{pkgName}}.server.**.dao")
@EnableConfigurationProperties(ClapSysLogProperties.class)
@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class,args);
    }
}
