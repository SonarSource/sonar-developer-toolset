/*
 * Copyright header
 */

package sample;


// order of imports : libs by alphabetical order, then javax, then java

import com.google.common.collect.Maps;

import javax.activation.CommandMap;
import java.util.Map;

@Annotation(param1 = "value1", param2 = "value2")
public abstract class Codestyle {

  public int[] X = new int[]{1, 3, 5, 7, 9, 11};

  @Annotation(param1 = "value1", param2 = "value2")
  public void foo(boolean a, int x, int y, int z) {
    Map map = Maps.newHashMap();
    CommandMap commandMap = null;
    try {
      String[] multipleLinesDeclaration = {
        "one",
        "two",
        "three"
      };
    } catch (Exception e) {
      processException(e.getMessage(), x + y, z, a);
    } finally {
      processFinally();
    }

    switch (x) {
      case 0:
        doCase0();
        break;
      default:
        doDefault();
    }

    if (2 < 3) {
      return;
    } else if (2 > 3) {
      return;
    } else {
      return;
    }

    do {
      x++;
    } while (x < 10000);

    while (x < 50000) {
      x++;
    }

    for (int i = 0; i < 5; i++) {
      System.out.println(i);
    }
  }

  /**
   * This is a method description that is long enough to exceed right margin.
   * <p/>
   * Another paragraph of the description placed after blank line.
   * <p/>
   * Line with manual
   * line feed.
   *
   * @param i                  short named parameter description
   * @param longParameterName  long named parameter description
   * @param missingDescription
   * @return return description.
   * @throws XXXException description.
   * @throws YException   description.
   * @throws ZException
   * @invalidTag
   */
  public abstract String sampleMethod(int i, int longParameterName, int missingDescription) throws XXXException, YException, ZException;

  /**
   * One-line comment
   */
  public String sampleMethod2() {
    // single-line comment
    int i = 0;
  }

  private final void orderOfVisibilityModifiers() {
  }

  private class InnerClass implements I1, I2 {
    public void bar() throws E1, E2 {
    }
  }
}