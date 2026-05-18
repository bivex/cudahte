# Generated from CUDAParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .CUDAParser import CUDAParser
else:
    from CUDAParser import CUDAParser

# This class defines a complete generic visitor for a parse tree produced by CUDAParser.

class CUDAParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by CUDAParser#translationUnit.
    def visitTranslationUnit(self, ctx:CUDAParser.TranslationUnitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#primaryExpression.
    def visitPrimaryExpression(self, ctx:CUDAParser.PrimaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#idExpression.
    def visitIdExpression(self, ctx:CUDAParser.IdExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#unqualifiedId.
    def visitUnqualifiedId(self, ctx:CUDAParser.UnqualifiedIdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#qualifiedId.
    def visitQualifiedId(self, ctx:CUDAParser.QualifiedIdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#nestedNameSpecifier.
    def visitNestedNameSpecifier(self, ctx:CUDAParser.NestedNameSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#lambdaExpression.
    def visitLambdaExpression(self, ctx:CUDAParser.LambdaExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#lambdaIntroducer.
    def visitLambdaIntroducer(self, ctx:CUDAParser.LambdaIntroducerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#lambdaCapture.
    def visitLambdaCapture(self, ctx:CUDAParser.LambdaCaptureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#captureDefault.
    def visitCaptureDefault(self, ctx:CUDAParser.CaptureDefaultContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#captureList.
    def visitCaptureList(self, ctx:CUDAParser.CaptureListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#capture.
    def visitCapture(self, ctx:CUDAParser.CaptureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#simpleCapture.
    def visitSimpleCapture(self, ctx:CUDAParser.SimpleCaptureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#initCapture.
    def visitInitCapture(self, ctx:CUDAParser.InitCaptureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#lambdaDeclarator.
    def visitLambdaDeclarator(self, ctx:CUDAParser.LambdaDeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#postfixExpression.
    def visitPostfixExpression(self, ctx:CUDAParser.PostfixExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#typeIdOfTheTypeId.
    def visitTypeIdOfTheTypeId(self, ctx:CUDAParser.TypeIdOfTheTypeIdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#expressionList.
    def visitExpressionList(self, ctx:CUDAParser.ExpressionListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#pseudoDestructorName.
    def visitPseudoDestructorName(self, ctx:CUDAParser.PseudoDestructorNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#unaryExpression.
    def visitUnaryExpression(self, ctx:CUDAParser.UnaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#unaryOperator.
    def visitUnaryOperator(self, ctx:CUDAParser.UnaryOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#newExpression_.
    def visitNewExpression_(self, ctx:CUDAParser.NewExpression_Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#newPlacement.
    def visitNewPlacement(self, ctx:CUDAParser.NewPlacementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#newTypeId.
    def visitNewTypeId(self, ctx:CUDAParser.NewTypeIdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#newDeclarator_.
    def visitNewDeclarator_(self, ctx:CUDAParser.NewDeclarator_Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#noPointerNewDeclarator.
    def visitNoPointerNewDeclarator(self, ctx:CUDAParser.NoPointerNewDeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#newInitializer_.
    def visitNewInitializer_(self, ctx:CUDAParser.NewInitializer_Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#deleteExpression.
    def visitDeleteExpression(self, ctx:CUDAParser.DeleteExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#noExceptExpression.
    def visitNoExceptExpression(self, ctx:CUDAParser.NoExceptExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#castExpression.
    def visitCastExpression(self, ctx:CUDAParser.CastExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#pointerMemberExpression.
    def visitPointerMemberExpression(self, ctx:CUDAParser.PointerMemberExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#multiplicativeExpression.
    def visitMultiplicativeExpression(self, ctx:CUDAParser.MultiplicativeExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#additiveExpression.
    def visitAdditiveExpression(self, ctx:CUDAParser.AdditiveExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#shiftExpression.
    def visitShiftExpression(self, ctx:CUDAParser.ShiftExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#shiftOperator.
    def visitShiftOperator(self, ctx:CUDAParser.ShiftOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#relationalExpression.
    def visitRelationalExpression(self, ctx:CUDAParser.RelationalExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#equalityExpression.
    def visitEqualityExpression(self, ctx:CUDAParser.EqualityExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#andExpression.
    def visitAndExpression(self, ctx:CUDAParser.AndExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#exclusiveOrExpression.
    def visitExclusiveOrExpression(self, ctx:CUDAParser.ExclusiveOrExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#inclusiveOrExpression.
    def visitInclusiveOrExpression(self, ctx:CUDAParser.InclusiveOrExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#logicalAndExpression.
    def visitLogicalAndExpression(self, ctx:CUDAParser.LogicalAndExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#logicalOrExpression.
    def visitLogicalOrExpression(self, ctx:CUDAParser.LogicalOrExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#conditionalExpression.
    def visitConditionalExpression(self, ctx:CUDAParser.ConditionalExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#assignmentExpression.
    def visitAssignmentExpression(self, ctx:CUDAParser.AssignmentExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#assignmentOperator.
    def visitAssignmentOperator(self, ctx:CUDAParser.AssignmentOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#expression.
    def visitExpression(self, ctx:CUDAParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#constantExpression.
    def visitConstantExpression(self, ctx:CUDAParser.ConstantExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#statement.
    def visitStatement(self, ctx:CUDAParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#labeledStatement.
    def visitLabeledStatement(self, ctx:CUDAParser.LabeledStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#expressionStatement.
    def visitExpressionStatement(self, ctx:CUDAParser.ExpressionStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#compoundStatement.
    def visitCompoundStatement(self, ctx:CUDAParser.CompoundStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#statementSeq.
    def visitStatementSeq(self, ctx:CUDAParser.StatementSeqContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#selectionStatement.
    def visitSelectionStatement(self, ctx:CUDAParser.SelectionStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#condition.
    def visitCondition(self, ctx:CUDAParser.ConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#iterationStatement.
    def visitIterationStatement(self, ctx:CUDAParser.IterationStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#forInitStatement.
    def visitForInitStatement(self, ctx:CUDAParser.ForInitStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#forRangeDeclaration.
    def visitForRangeDeclaration(self, ctx:CUDAParser.ForRangeDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#forRangeInitializer.
    def visitForRangeInitializer(self, ctx:CUDAParser.ForRangeInitializerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#jumpStatement.
    def visitJumpStatement(self, ctx:CUDAParser.JumpStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#declarationStatement.
    def visitDeclarationStatement(self, ctx:CUDAParser.DeclarationStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#declarationSeq.
    def visitDeclarationSeq(self, ctx:CUDAParser.DeclarationSeqContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#declaration.
    def visitDeclaration(self, ctx:CUDAParser.DeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#blockDeclaration.
    def visitBlockDeclaration(self, ctx:CUDAParser.BlockDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#aliasDeclaration.
    def visitAliasDeclaration(self, ctx:CUDAParser.AliasDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#simpleDeclaration.
    def visitSimpleDeclaration(self, ctx:CUDAParser.SimpleDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#staticAssertDeclaration.
    def visitStaticAssertDeclaration(self, ctx:CUDAParser.StaticAssertDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#emptyDeclaration_.
    def visitEmptyDeclaration_(self, ctx:CUDAParser.EmptyDeclaration_Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#attributeDeclaration.
    def visitAttributeDeclaration(self, ctx:CUDAParser.AttributeDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#declSpecifier.
    def visitDeclSpecifier(self, ctx:CUDAParser.DeclSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#declSpecifierSeq.
    def visitDeclSpecifierSeq(self, ctx:CUDAParser.DeclSpecifierSeqContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#storageClassSpecifier.
    def visitStorageClassSpecifier(self, ctx:CUDAParser.StorageClassSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#functionSpecifier.
    def visitFunctionSpecifier(self, ctx:CUDAParser.FunctionSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#typedefName.
    def visitTypedefName(self, ctx:CUDAParser.TypedefNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#typeSpecifier.
    def visitTypeSpecifier(self, ctx:CUDAParser.TypeSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#trailingTypeSpecifier.
    def visitTrailingTypeSpecifier(self, ctx:CUDAParser.TrailingTypeSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#typeSpecifierSeq.
    def visitTypeSpecifierSeq(self, ctx:CUDAParser.TypeSpecifierSeqContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#trailingTypeSpecifierSeq.
    def visitTrailingTypeSpecifierSeq(self, ctx:CUDAParser.TrailingTypeSpecifierSeqContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#simpleTypeLengthModifier.
    def visitSimpleTypeLengthModifier(self, ctx:CUDAParser.SimpleTypeLengthModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#simpleTypeSignednessModifier.
    def visitSimpleTypeSignednessModifier(self, ctx:CUDAParser.SimpleTypeSignednessModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#simpleTypeSpecifier.
    def visitSimpleTypeSpecifier(self, ctx:CUDAParser.SimpleTypeSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#theTypeName.
    def visitTheTypeName(self, ctx:CUDAParser.TheTypeNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#decltypeSpecifier.
    def visitDecltypeSpecifier(self, ctx:CUDAParser.DecltypeSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#elaboratedTypeSpecifier.
    def visitElaboratedTypeSpecifier(self, ctx:CUDAParser.ElaboratedTypeSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#enumName.
    def visitEnumName(self, ctx:CUDAParser.EnumNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#enumSpecifier.
    def visitEnumSpecifier(self, ctx:CUDAParser.EnumSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#enumHead.
    def visitEnumHead(self, ctx:CUDAParser.EnumHeadContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#opaqueEnumDeclaration.
    def visitOpaqueEnumDeclaration(self, ctx:CUDAParser.OpaqueEnumDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#enumKey.
    def visitEnumKey(self, ctx:CUDAParser.EnumKeyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#enumBase.
    def visitEnumBase(self, ctx:CUDAParser.EnumBaseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#enumeratorList.
    def visitEnumeratorList(self, ctx:CUDAParser.EnumeratorListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#enumeratorDefinition.
    def visitEnumeratorDefinition(self, ctx:CUDAParser.EnumeratorDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#enumerator.
    def visitEnumerator(self, ctx:CUDAParser.EnumeratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#namespaceName.
    def visitNamespaceName(self, ctx:CUDAParser.NamespaceNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#originalNamespaceName.
    def visitOriginalNamespaceName(self, ctx:CUDAParser.OriginalNamespaceNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#namespaceDefinition.
    def visitNamespaceDefinition(self, ctx:CUDAParser.NamespaceDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#namespaceAlias.
    def visitNamespaceAlias(self, ctx:CUDAParser.NamespaceAliasContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#namespaceAliasDefinition.
    def visitNamespaceAliasDefinition(self, ctx:CUDAParser.NamespaceAliasDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#qualifiedNamespaceSpecifier.
    def visitQualifiedNamespaceSpecifier(self, ctx:CUDAParser.QualifiedNamespaceSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#usingDeclaration.
    def visitUsingDeclaration(self, ctx:CUDAParser.UsingDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#usingDirective.
    def visitUsingDirective(self, ctx:CUDAParser.UsingDirectiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#asmDefinition.
    def visitAsmDefinition(self, ctx:CUDAParser.AsmDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#linkageSpecification.
    def visitLinkageSpecification(self, ctx:CUDAParser.LinkageSpecificationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#attributeSpecifierSeq.
    def visitAttributeSpecifierSeq(self, ctx:CUDAParser.AttributeSpecifierSeqContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#attributeSpecifier.
    def visitAttributeSpecifier(self, ctx:CUDAParser.AttributeSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#alignmentSpecifier.
    def visitAlignmentSpecifier(self, ctx:CUDAParser.AlignmentSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#attributeList.
    def visitAttributeList(self, ctx:CUDAParser.AttributeListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#attribute.
    def visitAttribute(self, ctx:CUDAParser.AttributeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#attributeNamespace.
    def visitAttributeNamespace(self, ctx:CUDAParser.AttributeNamespaceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#attributeArgumentClause.
    def visitAttributeArgumentClause(self, ctx:CUDAParser.AttributeArgumentClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#balancedTokenSeq.
    def visitBalancedTokenSeq(self, ctx:CUDAParser.BalancedTokenSeqContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#balancedToken.
    def visitBalancedToken(self, ctx:CUDAParser.BalancedTokenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#initDeclaratorList.
    def visitInitDeclaratorList(self, ctx:CUDAParser.InitDeclaratorListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#initDeclarator.
    def visitInitDeclarator(self, ctx:CUDAParser.InitDeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#declarator.
    def visitDeclarator(self, ctx:CUDAParser.DeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#pointerDeclarator.
    def visitPointerDeclarator(self, ctx:CUDAParser.PointerDeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#noPointerDeclarator.
    def visitNoPointerDeclarator(self, ctx:CUDAParser.NoPointerDeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#parametersAndQualifiers.
    def visitParametersAndQualifiers(self, ctx:CUDAParser.ParametersAndQualifiersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#trailingReturnType.
    def visitTrailingReturnType(self, ctx:CUDAParser.TrailingReturnTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#pointerOperator.
    def visitPointerOperator(self, ctx:CUDAParser.PointerOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#cvQualifierSeq.
    def visitCvQualifierSeq(self, ctx:CUDAParser.CvQualifierSeqContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#cvQualifier.
    def visitCvQualifier(self, ctx:CUDAParser.CvQualifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#refQualifier.
    def visitRefQualifier(self, ctx:CUDAParser.RefQualifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#declaratorId.
    def visitDeclaratorId(self, ctx:CUDAParser.DeclaratorIdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#theTypeId.
    def visitTheTypeId(self, ctx:CUDAParser.TheTypeIdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#abstractDeclarator.
    def visitAbstractDeclarator(self, ctx:CUDAParser.AbstractDeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#pointerAbstractDeclarator.
    def visitPointerAbstractDeclarator(self, ctx:CUDAParser.PointerAbstractDeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#noPointerAbstractDeclarator.
    def visitNoPointerAbstractDeclarator(self, ctx:CUDAParser.NoPointerAbstractDeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#abstractPackDeclarator.
    def visitAbstractPackDeclarator(self, ctx:CUDAParser.AbstractPackDeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#noPointerAbstractPackDeclarator.
    def visitNoPointerAbstractPackDeclarator(self, ctx:CUDAParser.NoPointerAbstractPackDeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#parameterDeclarationClause.
    def visitParameterDeclarationClause(self, ctx:CUDAParser.ParameterDeclarationClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#parameterDeclarationList.
    def visitParameterDeclarationList(self, ctx:CUDAParser.ParameterDeclarationListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#parameterDeclaration.
    def visitParameterDeclaration(self, ctx:CUDAParser.ParameterDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#functionDefinition.
    def visitFunctionDefinition(self, ctx:CUDAParser.FunctionDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#functionBody.
    def visitFunctionBody(self, ctx:CUDAParser.FunctionBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#initializer.
    def visitInitializer(self, ctx:CUDAParser.InitializerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#braceOrEqualInitializer.
    def visitBraceOrEqualInitializer(self, ctx:CUDAParser.BraceOrEqualInitializerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#initializerClause.
    def visitInitializerClause(self, ctx:CUDAParser.InitializerClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#initializerList.
    def visitInitializerList(self, ctx:CUDAParser.InitializerListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#bracedInitList.
    def visitBracedInitList(self, ctx:CUDAParser.BracedInitListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#className.
    def visitClassName(self, ctx:CUDAParser.ClassNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#classSpecifier.
    def visitClassSpecifier(self, ctx:CUDAParser.ClassSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#classHead.
    def visitClassHead(self, ctx:CUDAParser.ClassHeadContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#classHeadName.
    def visitClassHeadName(self, ctx:CUDAParser.ClassHeadNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#classVirtSpecifier.
    def visitClassVirtSpecifier(self, ctx:CUDAParser.ClassVirtSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#classKey.
    def visitClassKey(self, ctx:CUDAParser.ClassKeyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#memberSpecification.
    def visitMemberSpecification(self, ctx:CUDAParser.MemberSpecificationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#memberDeclaration.
    def visitMemberDeclaration(self, ctx:CUDAParser.MemberDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#memberDeclaratorList.
    def visitMemberDeclaratorList(self, ctx:CUDAParser.MemberDeclaratorListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#memberDeclarator.
    def visitMemberDeclarator(self, ctx:CUDAParser.MemberDeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#virtualSpecifierSeq.
    def visitVirtualSpecifierSeq(self, ctx:CUDAParser.VirtualSpecifierSeqContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#virtualSpecifier.
    def visitVirtualSpecifier(self, ctx:CUDAParser.VirtualSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#pureSpecifier.
    def visitPureSpecifier(self, ctx:CUDAParser.PureSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#baseClause.
    def visitBaseClause(self, ctx:CUDAParser.BaseClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#baseSpecifierList.
    def visitBaseSpecifierList(self, ctx:CUDAParser.BaseSpecifierListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#baseSpecifier.
    def visitBaseSpecifier(self, ctx:CUDAParser.BaseSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#classOrDeclType.
    def visitClassOrDeclType(self, ctx:CUDAParser.ClassOrDeclTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#baseTypeSpecifier.
    def visitBaseTypeSpecifier(self, ctx:CUDAParser.BaseTypeSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#accessSpecifier.
    def visitAccessSpecifier(self, ctx:CUDAParser.AccessSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#conversionFunctionId.
    def visitConversionFunctionId(self, ctx:CUDAParser.ConversionFunctionIdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#conversionTypeId.
    def visitConversionTypeId(self, ctx:CUDAParser.ConversionTypeIdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#conversionDeclarator.
    def visitConversionDeclarator(self, ctx:CUDAParser.ConversionDeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#constructorInitializer.
    def visitConstructorInitializer(self, ctx:CUDAParser.ConstructorInitializerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#memInitializerList.
    def visitMemInitializerList(self, ctx:CUDAParser.MemInitializerListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#memInitializer.
    def visitMemInitializer(self, ctx:CUDAParser.MemInitializerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#memInitializerId.
    def visitMemInitializerId(self, ctx:CUDAParser.MemInitializerIdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#operatorFunctionId.
    def visitOperatorFunctionId(self, ctx:CUDAParser.OperatorFunctionIdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#literalOperatorId.
    def visitLiteralOperatorId(self, ctx:CUDAParser.LiteralOperatorIdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#templateDeclaration.
    def visitTemplateDeclaration(self, ctx:CUDAParser.TemplateDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#templateParameterList.
    def visitTemplateParameterList(self, ctx:CUDAParser.TemplateParameterListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#templateParameter.
    def visitTemplateParameter(self, ctx:CUDAParser.TemplateParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#typeParameter.
    def visitTypeParameter(self, ctx:CUDAParser.TypeParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#simpleTemplateId.
    def visitSimpleTemplateId(self, ctx:CUDAParser.SimpleTemplateIdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#templateId.
    def visitTemplateId(self, ctx:CUDAParser.TemplateIdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#templateName.
    def visitTemplateName(self, ctx:CUDAParser.TemplateNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#templateArgumentList.
    def visitTemplateArgumentList(self, ctx:CUDAParser.TemplateArgumentListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#templateArgument.
    def visitTemplateArgument(self, ctx:CUDAParser.TemplateArgumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#typeNameSpecifier.
    def visitTypeNameSpecifier(self, ctx:CUDAParser.TypeNameSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#explicitInstantiation.
    def visitExplicitInstantiation(self, ctx:CUDAParser.ExplicitInstantiationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#explicitSpecialization.
    def visitExplicitSpecialization(self, ctx:CUDAParser.ExplicitSpecializationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#tryBlock.
    def visitTryBlock(self, ctx:CUDAParser.TryBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#functionTryBlock.
    def visitFunctionTryBlock(self, ctx:CUDAParser.FunctionTryBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#handlerSeq.
    def visitHandlerSeq(self, ctx:CUDAParser.HandlerSeqContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#handler.
    def visitHandler(self, ctx:CUDAParser.HandlerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#exceptionDeclaration.
    def visitExceptionDeclaration(self, ctx:CUDAParser.ExceptionDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#throwExpression.
    def visitThrowExpression(self, ctx:CUDAParser.ThrowExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#exceptionSpecification.
    def visitExceptionSpecification(self, ctx:CUDAParser.ExceptionSpecificationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#dynamicExceptionSpecification.
    def visitDynamicExceptionSpecification(self, ctx:CUDAParser.DynamicExceptionSpecificationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#typeIdList.
    def visitTypeIdList(self, ctx:CUDAParser.TypeIdListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#noExceptSpecification.
    def visitNoExceptSpecification(self, ctx:CUDAParser.NoExceptSpecificationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#theOperator.
    def visitTheOperator(self, ctx:CUDAParser.TheOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CUDAParser#literal.
    def visitLiteral(self, ctx:CUDAParser.LiteralContext):
        return self.visitChildren(ctx)



del CUDAParser