import io.circe.syntax.EncoderOps
import io.circe.{Json, JsonObject}
import Assertions.{CONST, CONTAINS, DEF, DEFINITIONS, DEPENDENTREQUIRED, DEPENDENTSCHEMAS, DESCRIPTION, ELSE, ENUM, EXCLUSIVEMAXIMUM, EXCLUSIVEMINIMUM, ID, ID2, IF, ITEMS, MAXCONTAINS, MAXIMUM, MINCONTAINS, MINIMUM, OTHER_ASSERTIONS, PATTERNPROPERTIES, PREFIXITEMS, PROPERTIES, REF, RELEVANT_ASSERTIONS, SCHEMA, THEN, UNIQUEITEMS}

object DraftTranslation {

  def modifyExclusive(assertion1: String, assertion2: String, s: JsonObject): JsonObject = {
    var obj = s
    obj.apply(assertion1).get.name match {
      case "Boolean" => Option(obj.apply(assertion2)) match {
        // if xMin or xMax are false just remove them
        case Some(Some(m)) => if(obj.apply(assertion1).get.asBoolean.get) obj = obj.remove(assertion1).add(assertion1,m)
        else obj = obj.remove(assertion1)
        case _ => obj = obj.remove(assertion1)
      }
      case _ =>
    }

    obj
  }
  def translate(s: Json): Json = {

    val assertions = RELEVANT_ASSERTIONS.union(OTHER_ASSERTIONS)

    s.name match {
      case "Object" =>
        var sAsObj = s.asObject.get
        val keys = sAsObj.keys

        keys.foreach {
          k => if(!assertions.contains(k)) sAsObj = sAsObj.remove(k)
        }

        if(sAsObj.contains(EXCLUSIVEMINIMUM))
          sAsObj = modifyExclusive(EXCLUSIVEMINIMUM,MINIMUM,sAsObj)

        if(sAsObj.contains(EXCLUSIVEMAXIMUM))
          sAsObj = modifyExclusive(EXCLUSIVEMAXIMUM,MAXIMUM,sAsObj)

        if(sAsObj.contains(ITEMS)) {
          sAsObj.apply(ITEMS).get.name match {
            case "Array" => val itemsTuple = sAsObj.apply(ITEMS).get
              sAsObj = sAsObj.remove(ITEMS).add(PREFIXITEMS,itemsTuple)
            case _ =>
          }
        }
        if(sAsObj.contains("additionalItems")) {
          val addItems = if(sAsObj.contains(ITEMS) && sAsObj.apply(ITEMS).get.name.equals("Object")) sAsObj.apply(ITEMS).get
          else sAsObj.apply("additionalItems").get
          sAsObj = sAsObj.remove("additionalItems").add(ITEMS,addItems)
        }

        if(sAsObj.contains("dependencies")) {
          val schemaDependencies = sAsObj.apply("dependencies").get
          var dependentRequired = JsonObject.empty
          var dependentSchemas = JsonObject.empty

          schemaDependencies.name match {
            case "Object" => schemaDependencies.asObject.get.toMap.foreach {
              case (k, v) => v.name match {
                case "Object" => dependentSchemas = dependentSchemas.add(k, v)
                case "Array" => dependentRequired = dependentRequired.add(k, v)
                case _ =>
              }
            }
            case _ =>
          }

          sAsObj = sAsObj.remove("dependencies")
          if(dependentRequired.size>0) sAsObj = sAsObj.add(DEPENDENTREQUIRED,dependentRequired.asJson)
          if(dependentSchemas.size>0) {
            sAsObj = sAsObj.add(DEPENDENTSCHEMAS,dependentSchemas.asJson)
          }

        }

        if(sAsObj.contains(REF)) {
          if(sAsObj.apply(REF).get.name.equals("String")) {
            if(sAsObj.apply(REF).get.asString.get.contains(DEFINITIONS)) {
              val refValue = sAsObj.apply(REF).get.asString.get
              val newRefValue = refValue.replaceAll(DEFINITIONS,"\\$defs")
              sAsObj = sAsObj.remove(REF).add(REF,newRefValue.asJson)
            }
          }
        }

        if(sAsObj.contains(SCHEMA))
          sAsObj = sAsObj.remove(SCHEMA)

        if(sAsObj.contains(ID))
          sAsObj = sAsObj.remove(ID)

        if(sAsObj.contains(ID2))
          sAsObj = sAsObj.remove(ID2)

        if(sAsObj.contains(DESCRIPTION))
          sAsObj = sAsObj.remove(DESCRIPTION)

        if(sAsObj.contains("version"))
          sAsObj = sAsObj.remove("version")

        if(sAsObj.contains("title"))
          sAsObj = sAsObj.remove("title")

        if(sAsObj.contains(DEFINITIONS)) {
          val defs = sAsObj.apply(DEFINITIONS).get
          sAsObj = sAsObj.remove(DEFINITIONS).add(DEF,defs)
        }

        if(sAsObj.contains("_format")) {
          val formatVal = sAsObj.apply("_format").get
          sAsObj = sAsObj.remove("_format").add("format",formatVal)
        }

        if(sAsObj.contains("_uniqueItems")) {
          val uniqueItemsVal = sAsObj.apply("_uniqueItems").get
          sAsObj = sAsObj.remove("_uniqueItems").add(UNIQUEITEMS,uniqueItemsVal)
        }

        if(!sAsObj.contains(IF)) {
          if(sAsObj.contains(THEN)) sAsObj = sAsObj.remove(THEN)
          if(sAsObj.contains(ELSE)) sAsObj = sAsObj.remove(ELSE)
        }

        if (!sAsObj.contains(CONTAINS)) {
          if (sAsObj.contains(MINCONTAINS)) sAsObj = sAsObj.remove(MINCONTAINS)
          if (sAsObj.contains(MAXCONTAINS)) sAsObj = sAsObj.remove(MAXCONTAINS)
        }

        sAsObj = JsonObject.fromMap(sAsObj.toMap.map{
          case (k,v) =>

            if(v.name.equals("Object") && !k.equals(CONST)) {
            if(k.equals(PROPERTIES) || k.equals(PATTERNPROPERTIES) || k.equals(DEF) || k.equals(DEFINITIONS)) {
              (k,v.asObject.get.mapValues(x => translate(x)).asJson)
            }
            else
              (k,translate(v))
          }
          else if(v.name.equals("Array") && !k.equals(ENUM)) (k,v.asArray.get.map(i => translate(i)).asJson)
          else (k,v)
        })
        sAsObj.asJson

      case _ => s
    }

  }
}
